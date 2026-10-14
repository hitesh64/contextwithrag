import io
import json

from openpyxl import Workbook

from backend.app.core import database
from backend.app.core.config import settings
from backend.app.services import llm

from .conftest import API

CSV = """asset_code,reported_at,symptoms,error_code,downtime_minutes,root_cause,corrective_action,parts_used,resolution_status,source_record_id
CNC-01,2026-01-15 09:30,Spindle overheating alarm,E-204,120,Coolant pump failed,Replaced coolant pump,CP-12,resolved,LOG-1
cnc-01,2026-02-20,Spindle overheating alarm,E-204,90,,Cleaned coolant filter,,resolved,LOG-2
CNC-01,10/03/2026 14:00,Chuck does not clamp,,,,,,open,LOG-3
NOPE-99,2026-01-01,Unknown machine,,,,,,open,LOG-4
CNC-01,not a date,Bad date,,,,,,open,LOG-5
CNC-01,2026-01-05,,,,,,,open,LOG-6
CNC-01,2026-01-06,Negative downtime,,-5,,,,open,LOG-7
CNC-01,2026-01-07,Bad status,,,,,,exploded,LOG-8
CNC-01,2999-01-01,From the future,,,,,,open,LOG-9
"""


def import_file(client, who, name, data, **params):
    return client.post(f"{API}/breakdowns/import", headers=who, files={"file": (name, data)}, params=params)


# ---------- breakdowns ----------

def test_import_takes_valid_rows_and_explains_every_rejected_one(client, factory, monkeypatch):
    asset = factory.asset("CNC-01")
    preview = import_file(client, factory.admin, "log.csv", CSV.encode(), dry_run=True).json()
    assert preview["valid"] == 3 and preview["imported"] == 0
    assert database.breakdowns.count_documents({}) == 0

    result = import_file(client, factory.admin, "log.csv", CSV.encode()).json()
    assert result["imported"] == 3 and result["rejected"] == 6 and result["total_rows"] == 9
    reasons = {e["row"]: e["error"] for e in result["errors"]}
    assert "unknown asset_code NOPE-99" in reasons[5]
    assert "not a date" in reasons[6] and "symptoms is empty" in reasons[7]
    assert "negative" in reasons[8] and "resolution_status" in reasons[9] and "future" in reasons[10]

    records = list(database.breakdowns.find().sort("reported_at", 1))
    assert all(r["asset_id"] == asset["id"] and r["organization_id"] == factory.organization_id for r in records)
    # A cell left empty stays unknown; it is not turned into text or a guess
    assert records[1]["root_cause"] is None and records[2]["downtime_minutes"] is None
    assert records[2]["reported_at"].strftime("%Y-%m-%d %H:%M") == "2026-03-10 14:00"

    # A time without a zone is the factory's local time
    monkeypatch.setattr(settings, "LOCAL_TIMEZONE", "Asia/Kolkata")
    local = import_file(client, factory.admin, "one.csv", b"asset_code,reported_at,symptoms\nCNC-01,2026-03-11 14:00,Local time\n")
    assert local.json()["imported"] == 1
    assert database.breakdowns.find_one({"symptoms": "Local time"})["reported_at"].strftime("%H:%M") == "08:30"
    database.breakdowns.delete_one({"symptoms": "Local time"})

    # The same file again adds nothing
    again = import_file(client, factory.admin, "log.csv", CSV.encode()).json()
    assert again["imported"] == 0 and again["skipped_duplicates"] == 3
    assert database.breakdowns.count_documents({}) == 3


def test_excel_import_and_bad_files(client, factory):
    factory.asset("CNC-01")
    book = Workbook()
    book.active.append(["Asset_Code", "Reported_At", "Symptoms", "Downtime_Minutes"])
    book.active.append(["CNC-01", "2026-04-01 10:00", "Tool turret jammed", 45])
    buffer = io.BytesIO()
    book.save(buffer)
    assert import_file(client, factory.admin, "log.xlsx", buffer.getvalue()).json()["imported"] == 1
    assert database.breakdowns.find_one({})["downtime_minutes"] == 45

    assert import_file(client, factory.admin, "log.csv", b"asset_code,symptoms\nCNC-01,x\n").status_code == 422
    assert import_file(client, factory.admin, "log.xlsx", b"not an excel file").status_code == 422
    assert import_file(client, factory.admin, "log.pdf", b"%PDF-").status_code == 422
    assert import_file(client, factory.admin, "log.csv", b"").status_code == 422
    assert import_file(client, factory.user("technician"), "log.csv", CSV.encode()).status_code == 403


def test_search_filters_and_summary_of_recorded_facts(client, factory):
    asset, other = factory.asset("CNC-01"), factory.asset("PRESS-07")
    import_file(client, factory.admin, "log.csv", CSV.encode())
    factory.breakdown(other["id"], symptoms="Oil leak at the ram seal", downtime_minutes=30)

    def total(**params):
        return client.get(f"{API}/breakdowns", headers=factory.admin, params=params).json()["total"]

    assert total() == 4 and total(asset_id=asset["id"]) == 3 and total(status="open") == 2
    assert total(q="overheating") == 2 and total(error_code="e-204") == 2 and total(q="leak") == 1
    assert total(date_from="2026-02-01T00:00:00Z", date_to="2026-02-28T00:00:00Z") == 1

    summary = client.get(f"{API}/assets/{asset['id']}/breakdown-summary", headers=factory.admin).json()
    assert summary["total_records"] == 3 and summary["open_records"] == 1
    assert summary["total_downtime_minutes"] == 210
    repeat = summary["repeat_error_codes"][0]
    assert repeat["label"] == "E-204" and repeat["count"] == 2 and repeat["downtime_minutes"] == 210
    # Every figure points at records that exist
    stored = {str(r["_id"]) for r in database.breakdowns.find()}
    assert {r["id"] for r in repeat["records"]} <= stored
    assert summary["repeat_symptoms"][0]["label"] == "Spindle overheating alarm"
    # One recorded cause is not a repeat; two records have no cause at all and are reported as a gap
    assert summary["repeat_root_causes"] == []
    assert len(summary["data_gaps"]["root_cause_not_recorded"]) == 2
    assert len(summary["data_gaps"]["downtime_not_recorded"]) == 1


def test_breakdown_records_are_checked_and_scoped(client, factory, other_factory):
    asset = factory.asset("CNC-01")
    record = factory.breakdown(asset["id"], root_cause="")
    assert record["root_cause"] is None and record["record_no"] == "BD-0001"

    future = {"asset_id": asset["id"], "reported_at": "2999-01-01T00:00:00Z", "symptoms": "From the future"}
    assert client.post(f"{API}/breakdowns", headers=factory.admin, json=future).status_code == 422
    body = {"asset_id": asset["id"], "reported_at": "2026-03-01T08:00:00Z", "symptoms": "Stopped"}
    assert client.post(f"{API}/breakdowns", headers=factory.user("viewer"), json=body).status_code == 403
    # Another factory can neither see the record nor attach one to this asset
    assert client.post(f"{API}/breakdowns", headers=other_factory.admin, json=body).status_code == 404
    assert client.get(f"{API}/breakdowns", headers=other_factory.admin).json()["total"] == 0
    patch = client.patch(f"{API}/breakdowns/{record['id']}", headers=other_factory.admin, json={"root_cause": "x"})
    assert patch.status_code == 404

    fixed = client.patch(f"{API}/breakdowns/{record['id']}", headers=factory.user("technician"), json={
        "root_cause": "Worn belt", "resolution_status": "resolved",
    }).json()
    assert fixed["root_cause"] == "Worn belt" and fixed["resolution_status"] == "resolved"


# ---------- work orders ----------

SOP = (
    b"Lathe coolant SOP. Step 1: lock out and tag out the main isolator before opening the coolant tank. "
    b"Step 2: clean the coolant filter. Step 3: check the coolant pump CP-12 for noise."
)


def move(client, who, order_id, to, comment=""):
    return client.post(f"{API}/work-orders/{order_id}/transition", headers=who, json={"to": to, "comment": comment})


def manual_order(client, who, asset_id):
    created = client.post(f"{API}/work-orders", headers=who, json={
        "asset_id": asset_id, "title": "Replace coolant pump", "checklist": [{"step": "Isolate the electrical supply"}],
    })
    assert created.status_code == 201, created.text
    return created.json()


def test_generated_draft_is_grounded_flagged_and_changes_nothing_else(client, factory, fake_llm):
    asset = factory.asset("CNC-01")
    doc = factory.document("coolant_sop.txt", SOP, asset_ids=asset["id"])
    factory.breakdown(asset["id"], symptoms="Spindle overheating alarm", error_code="E-204")
    fake_llm.reply = json.dumps({
        "title": "Investigate spindle overheating on CNC-01",
        "description": "Alarm E-204 was recorded before [2]. The pump was sabotaged [9].",
        "priority": "urgent-ish",
        "checklist": [
            {"step": "Lock out and tag out the main isolator", "sources": [1]},
            {"step": "Clean the coolant filter", "sources": [1, 42]},
            {"step": "Replace the spindle bearings", "sources": []},
        ],
    })
    before = {name: database.db[name].count_documents({}) for name in ("assets", "documents", "breakdowns")}
    technician = factory.user("technician")
    response = client.post(f"{API}/work-orders/generate", headers=technician, json={
        "asset_id": asset["id"], "problem": "Spindle overheating alarm E-204 again",
    })
    assert response.status_code == 201, response.text
    order = response.json()

    assert order["status"] == "draft" and order["generated"] is True and order["order_no"] == "WO-0001"
    assert order["approved_by"] is None and order["executed_at"] is None
    assert order["priority"] == "medium"  # an unknown priority from the model is not accepted
    assert "[9]" not in order["description"]
    lockout, clean_filter, bearings = order["proposed_checklist"]
    assert lockout["safety_review"] is True and lockout["unsupported"] is False
    assert clean_filter["sources"] == [1]  # source 42 does not exist
    assert bearings["unsupported"] is True  # no evidence behind it: flagged for the reviewer
    references = {r["n"]: r for r in order["source_references"]}
    assert references[1]["document_id"] == doc["id"] and references[2]["type"] == "breakdown"
    assert fake_llm.calls[-1]["json_output"] is True
    # Generating a draft created exactly one work order and touched nothing else
    assert before == {name: database.db[name].count_documents({}) for name in before}
    assert database.work_orders.count_documents({}) == 1


def test_draft_without_evidence_or_with_a_broken_model_reply(client, factory, fake_llm):
    asset = factory.asset("CNC-01")
    body = {"asset_id": asset["id"], "problem": "Strange noise from the gearbox"}
    empty = client.post(f"{API}/work-orders/generate", headers=factory.admin, json=body).json()
    assert fake_llm.calls == [] and empty["proposed_checklist"] == [] and empty["generated"] is False
    assert "Write the checks manually" in empty["description"]

    factory.document("coolant_sop.txt", SOP, asset_ids=asset["id"])
    fake_llm.reply = "Sure! Here is your work order: ..."
    assert client.post(f"{API}/work-orders/generate", headers=factory.admin, json=body).status_code == 503
    fake_llm.reply = llm.QuotaError("quota used up")
    assert client.post(f"{API}/work-orders/generate", headers=factory.admin, json=body).status_code == 429
    assert database.work_orders.count_documents({}) == 1
    assert client.post(f"{API}/work-orders/generate", headers=factory.user("viewer"), json=body).status_code == 403


def test_full_lifecycle_with_approval_and_audit(client, factory):
    asset = factory.asset("CNC-01")
    technician, manager = factory.user("technician"), factory.user("maintenance_manager")
    order = manual_order(client, technician, asset["id"])
    assert order["can_edit"] is True
    assert order["proposed_checklist"][0]["safety_review"] is True

    edited = client.patch(f"{API}/work-orders/{order['id']}", headers=technician, json={"priority": "high"})
    assert edited.json()["priority"] == "high"

    assert move(client, technician, order["id"], "pending_approval").status_code == 200
    # Frozen once submitted
    assert client.patch(f"{API}/work-orders/{order['id']}", headers=technician, json={"title": "Changed"}).status_code == 409
    assert move(client, technician, order["id"], "approved").status_code == 403
    assert move(client, technician, order["id"], "in_progress").status_code == 409

    approved = client.post(f"{API}/work-orders/{order['id']}/approve", headers=manager, json={"comment": "Go ahead"})
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved" and approved.json()["approved_by_name"] == "alpha maintenance_manager"
    assert approved.json()["approved_at"]

    assert move(client, technician, order["id"], "in_progress").json()["executed_at"]
    done = move(client, technician, order["id"], "completed", "Pump replaced").json()
    assert done["status"] == "completed" and done["completed_at"] and done["allowed_transitions"] == []
    assert [h["to"] for h in done["history"]] == ["draft", "pending_approval", "approved", "in_progress", "completed"]
    assert move(client, manager, order["id"], "cancelled").status_code == 409

    events = client.get(f"{API}/audit", headers=manager, params={"resource_type": "work_order"}).json()["items"]
    trail = [(e["action"], e["result"]) for e in reversed(events)]
    assert trail == [
        ("work_order.create", "success"), ("work_order.edit", "success"), ("work_order.pending_approval", "success"),
        ("work_order.approved", "denied"), ("work_order.in_progress", "denied"), ("work_order.approved", "success"),
        ("work_order.in_progress", "success"), ("work_order.completed", "success"), ("work_order.cancelled", "denied"),
    ]
    assert all(e["request_id"] and e["actor_name"] for e in events)


def test_approval_rules(client, factory, monkeypatch):
    asset = factory.asset("CNC-01")
    manager, second_manager, technician = factory.user("maintenance_manager"), factory.user("maintenance_manager"), factory.user("technician")

    own = manual_order(client, manager, asset["id"])
    move(client, manager, own["id"], "pending_approval")
    # Four-eyes rule: the author cannot approve their own work order
    assert move(client, manager, own["id"], "approved").status_code == 403
    assert move(client, second_manager, own["id"], "rejected").status_code == 422  # a reason is required
    rejected = move(client, second_manager, own["id"], "rejected", "Checklist is incomplete").json()
    assert rejected["status"] == "rejected" and rejected["history"][-1]["comment"] == "Checklist is incomplete"
    # Back to draft for rework, then approved by someone else
    assert move(client, technician, own["id"], "draft").status_code == 403  # not the author
    assert move(client, manager, own["id"], "draft").status_code == 200
    move(client, manager, own["id"], "pending_approval")
    assert move(client, second_manager, own["id"], "approved").status_code == 200

    monkeypatch.setattr(settings, "ALLOW_SELF_APPROVAL", True)
    solo = manual_order(client, manager, asset["id"])
    move(client, manager, solo["id"], "pending_approval")
    assert move(client, manager, solo["id"], "approved").status_code == 200

    # A draft cannot skip approval, and a technician cannot touch someone else's draft
    draft = manual_order(client, manager, asset["id"])
    assert move(client, manager, draft["id"], "in_progress").status_code == 409
    assert move(client, manager, draft["id"], "approved").status_code == 409
    assert move(client, technician, draft["id"], "pending_approval").status_code == 403
    assert client.patch(f"{API}/work-orders/{draft['id']}", headers=technician, json={"title": "Mine now"}).status_code == 403
    assert move(client, manager, draft["id"], "nonsense").status_code == 422


def test_work_orders_are_invisible_across_organizations(client, factory, other_factory):
    asset = factory.asset("CNC-01")
    order = manual_order(client, factory.admin, asset["id"])
    theirs = other_factory.admin
    assert client.get(f"{API}/work-orders", headers=theirs).json()["total"] == 0
    assert client.get(f"{API}/work-orders/{order['id']}", headers=theirs).status_code == 404
    assert move(client, theirs, order["id"], "cancelled").status_code == 404
    assert client.post(f"{API}/work-orders/{order['id']}/approve", headers=theirs).status_code == 404
    assert client.patch(f"{API}/work-orders/{order['id']}", headers=theirs, json={"title": "Hijacked"}).status_code == 404
    stolen = client.post(f"{API}/work-orders", headers=theirs, json={"asset_id": asset["id"], "title": "On their machine"})
    assert stolen.status_code == 404
    assert client.get(f"{API}/audit", headers=theirs).json()["items"][0]["action"] == "organization.create"
    assert all(e["organization_id"] == other_factory.organization_id for e in client.get(f"{API}/audit", headers=theirs).json()["items"])


def test_dashboard_counts_real_records_only(client, factory, other_factory):
    empty = client.get(f"{API}/dashboard", headers=factory.admin).json()
    assert empty["assets"] == {} and empty["downtime_by_asset"] == [] and empty["questions_asked"] == 0

    asset = factory.asset("CNC-01")
    other_factory.asset("CNC-01")
    recent = database.breakdowns  # reported "now" so that it falls inside the dashboard period
    from backend.app.core.utils import now
    factory.breakdown(asset["id"], downtime_minutes=40)
    recent.update_many({}, {"$set": {"reported_at": now()}})
    manual_order(client, factory.admin, asset["id"])

    board = client.get(f"{API}/dashboard", headers=factory.admin).json()
    assert board["assets"] == {"active": 1} and board["work_orders"] == {"draft": 1}
    assert board["downtime_by_asset"] == [{"asset_code": "CNC-01", "downtime_minutes": 40, "breakdowns": 1}]
    assert client.get(f"{API}/dashboard", headers=other_factory.admin).json()["downtime_by_asset"] == []


def test_dashboard_reliability_figures(client, factory, other_factory):
    """MTTR, MTBF and availability from the factory's own records, on the stated 24/7 basis."""
    from datetime import timedelta
    from backend.app.core.utils import now
    empty = client.get(f"{API}/dashboard", headers=factory.admin, params={"days": 30}).json()
    assert empty["kpis"] == {"breakdowns": 0, "downtime_minutes": 0, "mttr_minutes": None, "mtbf_hours": None,
                             "availability_pct": None, "assets_in_service": 0}
    assert len(empty["trend"]) in (30, 31) and empty["trend_step_days"] == 1

    press = factory.asset("PRS-01", criticality="critical")
    lathe = factory.asset("LTH-02", criticality="low")
    factory.asset("OLD-03", status="inactive")  # not in service: left out of the calendar time
    other_factory.asset("PRS-01")
    for asset, downtime, code, status in [(press, 120, "E-204", "resolved"), (press, 60, "e-204", "open"),
                                          (lathe, None, "", "resolved"), (lathe, 30, "OVL", "resolved")]:
        factory.breakdown(asset["id"], downtime_minutes=downtime, error_code=code or None, resolution_status=status)
    database.breakdowns.update_many({"organization_id": factory.organization_id}, {"$set": {"reported_at": now() - timedelta(days=2)}})

    board = client.get(f"{API}/dashboard", headers=factory.admin, params={"days": 30}).json()
    kpis = board["kpis"]
    assert kpis["breakdowns"] == 4 and kpis["downtime_minutes"] == 210 and kpis["assets_in_service"] == 2
    assert kpis["mttr_minutes"] == 70.0  # (120 + 60 + 30) / 3: the record without downtime is left out
    calendar = 30 * 24 * 2
    assert kpis["mtbf_hours"] == round((calendar - 3.5) / 4, 1)
    assert kpis["availability_pct"] == round(100 * (calendar - 3.5) / calendar, 2)
    assert sum(b["breakdowns"] for b in board["trend"]) == 4 and sum(b["downtime_minutes"] for b in board["trend"]) == 210
    assert board["top_error_codes"][0] == {"error_code": "E-204", "breakdowns": 2}
    assert [a["asset_code"] for a in board["repeat_assets"]] == ["PRS-01", "LTH-02"]
    assert board["attention"] == [{"asset_code": "PRS-01", "name": "Machine PRS-01", "criticality": "critical",
                                   "status": "active", "unresolved_breakdowns": 1}]
    assert board["assets_by_criticality"] == {"critical": 1, "low": 1, "high": 1}

    manual_order(client, factory.admin, press["id"])
    assert client.get(f"{API}/dashboard", headers=factory.admin).json()["work_orders_open_by_priority"] == {"medium": 1}
    assert client.get(f"{API}/dashboard", headers=other_factory.admin).json()["kpis"]["breakdowns"] == 0
