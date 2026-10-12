"""Conflicts between documents are found by the backend itself, answered without the model, and closed by people.

The documents here are small text files; the model is replaced by a fake that must not be asked when
the backend has already found a disagreement.
"""
from backend.app.core import database
from backend.app.services import conflicts as detector

from .conftest import API

QUESTION = (
    "After opening the pressure release valve on a hydraulic machine, how many minutes must I wait "
    "before loosening a fitting?"
)
PRESS = (
    b"Hydraulic press SOP. Open the pressure release valve and wait 10 minutes until the pressure gauge "
    b"reads 0 bar before loosening any hydraulic fitting."
)
GENERAL = (
    b"General lockout procedure. For hydraulic machines open the pressure release valve and wait 5 minutes; "
    b"for pneumatic machines vent the air line."
)


def ask(client, who, question=QUESTION, **extra):
    return client.post(f"{API}/chat", headers=who, json={"question": question, **extra}).json()


def number_of(prompt, filename):
    return prompt.split(f'] Document "{filename}"')[0].rsplit("[", 1)[1]


def patch_version(client, who, document, **fields):
    return client.patch(f"{API}/documents/{document['id']}/version", headers=who, json=fields)


# ---------- finding conflicts ----------

def test_two_sources_with_different_waiting_times_are_a_conflict_and_the_model_is_not_asked(client, factory, fake_llm):
    press_asset = factory.asset("PRESS-07")
    factory.document("press_sop.txt", PRESS, asset_ids=press_asset["id"])
    factory.document("general_lockout.txt", GENERAL)

    body = ask(client, factory.admin)
    assert fake_llm.calls == []
    assert body["conflict"] is True and body["review_required"] is False and body["insufficient_evidence"] is False
    answer = body["answer"]
    assert "Source A: 10 minutes" in answer and "Source B: 5 minutes" in answer
    assert 'Document "press_sop.txt"' in answer and 'Document "general_lockout.txt"' in answer
    assert "Status: Conflict unresolved." in answer and "qualified maintenance or safety supervisor" in answer
    # A general and a machine-specific document disagree: neither is made the winner
    assert "neither is assumed to take precedence" in answer
    assert {c["filename"] for c in body["citations"]} == {"press_sop.txt", "general_lockout.txt"}

    listed = client.get(f"{API}/conflicts?status=open", headers=factory.admin).json()
    assert listed["total"] == 1 and listed["items"][0]["kind"] == "conflict"
    assert body["conflicts"][0]["id"] == listed["items"][0]["id"]
    # Asking again does not create a second record
    ask(client, factory.admin)
    assert client.get(f"{API}/conflicts", headers=factory.admin).json()["total"] == 1


def test_three_sources_with_three_values_are_all_listed(client, factory, fake_llm):
    factory.document("press_sop.txt", PRESS)
    factory.document("general_lockout.txt", GENERAL)
    factory.document("plant_rules.txt", b"Plant rules. Open the pressure release valve and wait 15 minutes before loosening a hydraulic fitting.")

    body = ask(client, factory.admin)
    assert body["conflict"] is True and fake_llm.calls == []
    for expected in ("10 minutes", "5 minutes", "15 minutes", "Source C"):
        assert expected in body["answer"]
    assert len(body["citations"]) == 3


def test_a_superseded_document_is_not_a_conflict_but_only_when_a_manager_said_so(client, factory, fake_llm):
    old = factory.document("press_old.txt", PRESS)
    new = factory.document("press_new.txt", b"Hydraulic press SOP revision 4. Open the pressure release valve and wait 5 minutes before loosening any hydraulic fitting.")

    # Nothing says which is newer, so nothing is assumed: not from the names, not from the values
    unknown = ask(client, factory.admin)
    assert unknown["conflict"] is True and fake_llm.calls == []
    assert "Revision information is not recorded" in unknown["answer"] and "neither is assumed" in unknown["answer"].lower() or "Neither is assumed" in unknown["answer"]

    assert patch_version(client, factory.admin, new, supersedes_document_id=old["id"]).status_code == 200
    fake_llm.reply = lambda prompt, system: f"Wait 5 minutes [{number_of(prompt, 'press_new.txt')}]."
    settled = ask(client, factory.admin)
    assert settled["conflict"] is False and settled["review_required"] is False
    assert [s["filename"] for s in settled["superseded_sources"]] == ["press_old.txt"]
    assert 'Document "press_old.txt" (superseded revision)' in fake_llm.calls[-1]["prompt"]

    # The same through an explicit mark on the old document
    assert patch_version(client, factory.admin, new, supersedes_document_id=None).status_code == 200
    assert ask(client, factory.admin)["conflict"] is True
    assert patch_version(client, factory.admin, old, lifecycle="superseded", revision="2").status_code == 200
    assert ask(client, factory.admin)["conflict"] is False

    # A document cannot replace itself, and an unknown document is refused
    assert patch_version(client, factory.admin, new, supersedes_document_id=new["id"]).status_code == 422
    assert patch_version(client, factory.admin, new, supersedes_document_id="000000000000000000000000").status_code == 404
    assert patch_version(client, factory.admin, new).status_code == 422


def test_different_revisions_that_are_not_linked_stay_a_conflict_with_a_note(client, factory, fake_llm):
    one = factory.document("press_a.txt", PRESS)
    two = factory.document("press_b.txt", b"Hydraulic press SOP. Open the pressure release valve and wait 5 minutes before loosening any hydraulic fitting.")
    patch_version(client, factory.admin, one, revision="3", effective_date="2026-03-01")
    patch_version(client, factory.admin, two, revision="1", effective_date="2024-01-10")

    body = ask(client, factory.admin)
    assert body["conflict"] is True and fake_llm.calls == []
    assert "revision 3" in body["answer"] and "revision 1" in body["answer"]
    assert "none is marked as superseded" in body["answer"]


def test_documents_of_different_machines_are_not_compared(client, factory, fake_llm):
    lathe, compressor = factory.asset("CNC-01"), factory.asset("COMP-03")
    factory.document("lathe_sop.txt", PRESS, asset_ids=lathe["id"])
    factory.document("compressor_sop.txt", GENERAL.replace(b"General lockout procedure", b"Compressor procedure"), asset_ids=compressor["id"])

    fake_llm.reply = lambda prompt, system: f"Wait 10 minutes [{number_of(prompt, 'lathe_sop.txt')}]."
    body = ask(client, factory.admin)
    assert body["conflict"] is False and body["review_required"] is False and len(fake_llm.calls) == 1
    assert body["conflicts"] == []


def test_a_sentence_for_another_situation_is_ignored_and_unclear_conditions_need_review(client, factory, fake_llm):
    # The question says "hydraulic": a pneumatic-only sentence is not an alternative answer
    factory.document("press_sop.txt", PRESS)
    factory.document("air_sop.txt", b"Air system procedure. For pneumatic machines open the pressure release valve and wait 7 minutes before loosening any fitting.")
    fake_llm.reply = lambda prompt, system: f"Wait 10 minutes [{number_of(prompt, 'press_sop.txt')}]."
    assert ask(client, factory.admin)["conflict"] is False

    # Hot against cold oil, and the question does not say which: possibly different situations
    factory.document("gearbox_a.txt", b"Gearbox SOP A. Drain the hot oil and wait 10 minutes before opening the drain plug.")
    factory.document("gearbox_b.txt", b"Gearbox SOP B. Drain the cold oil and wait 5 minutes before opening the drain plug.")
    calls = len(fake_llm.calls)
    body = ask(client, factory.admin, "How long do I wait after draining the oil before opening the gearbox drain plug?")
    assert len(fake_llm.calls) == calls
    assert body["review_required"] is True and body["conflict"] is False
    assert "cold vs hot" in body["answer"] and "Review needed" in body["answer"]
    assert "Status: Conflict unresolved." not in body["answer"]
    assert body["conflicts"][0]["kind"] == "needs_review"


def test_equal_values_unrelated_numbers_and_ranges(client, factory, fake_llm):
    factory.document("sop_hours.txt", b"Press SOP. Open the pressure release valve and wait 1 hour before loosening a fitting. The oil tank holds 250 litres.")
    factory.document("sop_minutes.txt", b"Lockout SOP. Open the pressure release valve and wait 60 minutes before loosening a fitting. The oil tank holds 300 litres.")
    fake_llm.reply = lambda prompt, system: f"Wait 60 minutes [{number_of(prompt, 'sop_minutes.txt')}]."
    # 1 hour is 60 minutes; the litre figures are about something other than the question
    assert ask(client, factory.admin)["conflict"] is False

    # Overlapping but different ranges are not called a conflict outright
    factory.document("sop_range.txt", b"Valve SOP. Open the pressure release valve and wait 55 to 70 minutes before loosening a fitting.")
    body = ask(client, factory.admin)
    assert body["review_required"] is True and "overlapping ranges" in body["answer"]


def test_only_the_kind_of_quantity_the_question_asks_for_is_compared(client, factory, fake_llm):
    factory.document("press_sop.txt", PRESS)
    factory.document("general_lockout.txt", GENERAL)
    factory.document("compressor.txt", b"Compressor manual. The safety valve opens at a pressure of 11 bar and must be tested every month.")
    fake_llm.reply = lambda prompt, system: f"It opens at 11 bar [{number_of(prompt, 'compressor.txt')}]."
    body = ask(client, factory.admin, "At what pressure does the compressor safety valve open?")
    assert body["conflict"] is False and body["review_required"] is False and len(fake_llm.calls) == 1

    # The same kind of quantity in two documents is compared
    factory.document("compressor_b.txt", b"Compressor service sheet. The safety valve opens at a pressure of 10 bar and must be replaced when it leaks.")
    both = ask(client, factory.admin, "At what pressure does the compressor safety valve open?")
    assert both["conflict"] is True and "11 bar" in both["answer"] and "10 bar" in both["answer"]


def test_units_are_normalised_and_numbers_without_units_are_not_claims():
    claims = detector.extract_claims("Tighten to 45 N·m. Pressure 2.5 bar, never above 0.25 MPa. Wait ten minutes. Revision 3, page 12.", set())
    assert [(c["dimension"], round(c["low"], 3)) for c in claims] == [
        ("torque", 45), ("pressure", 2.5), ("pressure", 2.5), ("time", 10),
    ]


def test_numbers_written_as_words_are_read_whole():
    text = "Wait thirteen minutes. Run for sixty minutes. Wait six minutes. Cool for ninety minutes."
    assert [c["low"] for c in detector.extract_claims(text, set())] == [13, 60, 6, 90]


def test_a_unit_separated_from_its_number_is_read_but_never_from_inside_a_word():
    """Found by the evaluation: "every 500 operating hours" was missed, and "10 minutes until" read as 10 litres."""
    plan = detector.extract_claims("Replace the return filter every 500 operating hours.", set())
    assert [(c["dimension"], c["low"], c["value"]) for c in plan] == [("time", 500 * 60, "500 hours")]

    trap = detector.extract_claims("Wait 10 minutes until the gauge reads 0 bar before loosening the fitting.", set())
    # "until" must not supply the "l" of litres, and a gauge reading of 0 is not an instruction
    assert [(c["dimension"], c["low"]) for c in trap] == [("time", 10)]


def test_the_subject_of_a_claim_excludes_units_written_as_words():
    """Also from the evaluation: "degrees" and "C" counted as what the sentence was about."""
    claim = detector.extract_claims("Hydraulic oil temperature must stay below 60 degrees C during operation.", set())[0]
    assert "oil" in claim["key"] and "temperatur" in claim["key"]
    assert not {"c", "degre", "degrees"} & claim["key"]


def test_one_word_in_common_does_not_make_two_instructions_the_same(client, factory, fake_llm):
    """A compressor and a dryer both mention "shutdown"; that is not a disagreement about the same step."""
    factory.document("compressor.txt", b"Compressor manual. Before shutdown run the compressor for 5 minutes.")
    factory.document("dryer.txt", b"Dryer SOP. Wait 60 minutes after shutdown before opening the dryer cover.")
    fake_llm.reply = lambda prompt, system: f"Run it for 5 minutes [{number_of(prompt, 'compressor.txt')}]."
    body = ask(client, factory.admin, "How long should the compressor run before shutdown?")
    assert body["conflict"] is False and body["review_required"] is False and len(fake_llm.calls) == 1


def test_an_old_revision_is_named_only_where_it_answers_the_same_question(client, factory, fake_llm):
    """A question about cooling a furnace must not name an old pump revision that also mentions cooling."""
    old = factory.document("pump_rev1.txt", b"Pump SOP revision 1. After stopping the pump wait 30 minutes for the casing to cool before removing the cover.")
    new = factory.document("pump_rev2.txt", b"Pump SOP revision 2. After stopping the pump wait 45 minutes for the casing to cool before removing the cover.")
    factory.document("furnace_a.txt", b"Furnace manual. Allow the furnace to cool for 2 hours before opening the door.")
    assert patch_version(client, factory.admin, new, supersedes_document_id=old["id"]).status_code == 200

    fake_llm.reply = lambda prompt, system: f"Wait 45 minutes [{number_of(prompt, 'pump_rev2.txt')}]."
    pump = ask(client, factory.admin, "How long must I wait after stopping the pump before removing the cover?")
    assert [s["filename"] for s in pump["superseded_sources"]] == ["pump_rev1.txt"]

    fake_llm.reply = lambda prompt, system: f"Two hours [{number_of(prompt, 'furnace_a.txt')}]."
    furnace = ask(client, factory.admin, "How long must the furnace cool before opening the door?")
    assert furnace["superseded_sources"] == [] and furnace["conflict"] is False


def test_another_organizations_documents_are_never_compared(client, factory, other_factory, fake_llm):
    factory.document("press_sop.txt", PRESS)
    other_factory.document("their_sop.txt", GENERAL)
    fake_llm.reply = lambda prompt, system: f"Wait 10 minutes [{number_of(prompt, 'press_sop.txt')}]."
    body = ask(client, factory.admin)
    assert body["conflict"] is False and "their_sop.txt" not in fake_llm.calls[-1]["prompt"]
    assert client.get(f"{API}/conflicts", headers=other_factory.admin).json()["total"] == 0


def test_a_single_value_from_the_model_cannot_hide_a_conflict(client, factory, fake_llm):
    factory.document("press_sop.txt", PRESS)
    factory.document("general_lockout.txt", GENERAL)
    fake_llm.reply = lambda prompt, system: f"You must wait 10 minutes [{number_of(prompt, 'press_sop.txt')}]."
    body = ask(client, factory.admin)
    assert body["conflict"] is True and fake_llm.calls == []
    assert "You must wait" not in body["answer"]


# ---------- the lifecycle of a conflict ----------

def test_only_a_supervisor_or_admin_can_close_a_conflict_and_it_stays_visible(client, factory, fake_llm, monkeypatch):
    press = factory.document("press_sop.txt", PRESS)
    factory.document("general_lockout.txt", GENERAL)
    conflict_id = ask(client, factory.admin)["conflicts"][0]["id"]

    operator = factory.user("technician")
    viewer = factory.user("viewer")
    manager = factory.user("maintenance_manager")
    resolution = {"decision": "governs", "document_id": press["id"], "note": "The press manufacturer's manual says 10 minutes."}

    # Operators see the conflict but cannot close it; the refused attempt is audited
    assert client.get(f"{API}/conflicts/{conflict_id}", headers=operator).status_code == 200
    for who in (operator, viewer):
        assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=who, json=resolution).status_code == 403
    denied = list(database.audit_events.find({"action": "conflict.resolve", "result": "denied"}))
    assert len(denied) == 2 and denied[0]["resource_id"] == conflict_id
    assert client.get(f"{API}/conflicts/{conflict_id}", headers=manager).json()["status"] == "open"

    # A stricter company policy: admin only
    monkeypatch.setattr("backend.app.core.config.settings.CONFLICT_RESOLVE_ROLE", "admin")
    assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=manager, json=resolution).status_code == 403
    monkeypatch.setattr("backend.app.core.config.settings.CONFLICT_RESOLVE_ROLE", "maintenance_manager")

    # Bad requests: no note of substance, a document that is not part of the conflict
    assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=manager, json={**resolution, "note": "ok"}).status_code == 422
    assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=manager, json={**resolution, "document_id": None}).status_code == 422
    assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=manager, json={**resolution, "document_id": "000000000000000000000000"}).status_code == 422

    done = client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=manager, json=resolution)
    assert done.status_code == 200
    stored = done.json()
    assert stored["status"] == "resolved" and stored["resolution"]["decision"] == "governs"
    assert stored["resolution"]["resolved_by_name"] and stored["resolution"]["resolved_at"]
    assert {s["filename"] for s in stored["resolution"]["sources"]} == {"press_sop.txt", "general_lockout.txt"}
    event = database.audit_events.find_one({"action": "conflict.resolve", "result": "success"})
    assert event["resource_id"] == conflict_id and press["id"] in event["detail"]
    assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=manager, json=resolution).status_code == 409

    # Everyone now sees the recorded decision next to both original sources; the model is still not asked
    body = ask(client, operator)
    assert fake_llm.calls == [] and body["conflict"] is False
    assert "Resolved by" in body["answer"] and "this document governs (press_sop.txt)" in body["answer"]
    assert "Source A: 10 minutes" in body["answer"] and "Source B: 5 minutes" in body["answer"]
    assert "Check it against the approved procedure" in body["answer"]

    # The decision was about these documents as they were: a change to their version facts reopens it
    assert patch_version(client, factory.admin, press, revision="4").status_code == 200
    reopened = ask(client, operator)
    assert reopened["conflict"] is True and "Status: Conflict unresolved." in reopened["answer"]
    record = client.get(f"{API}/conflicts/{conflict_id}", headers=operator).json()
    assert record["status"] == "open" and len(record["history"]) == 1


def test_conflicts_of_another_organization_cannot_be_read_or_closed(client, factory, other_factory):
    factory.document("press_sop.txt", PRESS)
    factory.document("general_lockout.txt", GENERAL)
    conflict_id = ask(client, factory.admin)["conflicts"][0]["id"]
    theirs = other_factory.admin
    assert client.get(f"{API}/conflicts/{conflict_id}", headers=theirs).status_code == 404
    body = {"decision": "false_alarm", "note": "Looks fine to me, honestly."}
    assert client.post(f"{API}/conflicts/{conflict_id}/resolve", headers=theirs, json=body).status_code == 404
    assert client.get(f"{API}/conflicts/{conflict_id}", headers=factory.admin).json()["status"] == "open"
