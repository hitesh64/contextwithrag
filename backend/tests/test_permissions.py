"""Access chosen per user by the administrator: which sections are visible and what may be done in them."""
from backend.app.core import database
from backend.app.core.security import PERMISSIONS, role_permissions

from .conftest import API, PASSWORD
from .test_breakdowns_work_orders import manual_order, move


def person(client, factory, role: str, permissions: list[str] | None = None) -> tuple[dict, dict]:
    """(record, headers) of a new user; with permissions, the administrator's own choice for that user."""
    email = f"{role}{database.users.count_documents({})}@{factory.name}.example.com"
    body = {"name": f"{factory.name} {role}", "email": email, "password": PASSWORD, "role": role}
    if permissions is not None:
        body["permissions"] = permissions
    created = client.post(f"{API}/users", headers=factory.admin, json=body)
    assert created.status_code == 201, created.text
    return created.json(), factory.login(email)


def set_access(client, factory, user_id: str, permissions: list[str] | None):
    return client.patch(f"{API}/users/{user_id}", headers=factory.admin, json={"permissions": permissions})


def test_a_role_gives_its_standard_access(client, factory):
    viewer, headers = person(client, factory, "viewer")
    assert viewer["custom_permissions"] is False
    assert viewer["permissions"] == role_permissions("viewer") == client.get(f"{API}/auth/me", headers=headers).json()["permissions"]
    assert "work_orders.approve" not in role_permissions("technician")
    assert "work_orders.approve" in role_permissions("maintenance_manager")
    admin = client.get(f"{API}/auth/me", headers=factory.admin).json()
    assert set(admin["permissions"]) == {*PERMISSIONS, "users.manage"}

    catalogue = client.get(f"{API}/permissions", headers=factory.admin).json()
    assert [p["key"] for p in catalogue["permissions"]] == list(PERMISSIONS)
    assert catalogue["role_defaults"]["technician"] == role_permissions("technician")
    assert client.get(f"{API}/permissions", headers=headers).status_code == 403


def test_a_hidden_section_is_refused_by_the_server(client, factory):
    asset = factory.asset("CNC-01")
    factory.breakdown(asset["id"])
    user, headers = person(client, factory, "viewer", ["chat.ask", "assets.view"])
    assert user["custom_permissions"] is True and user["permissions"] == ["chat.ask", "assets.view"]

    for path in ("dashboard", "documents", "breakdowns", "work-orders", "conflicts", "audit", "chat/unanswered"):
        assert client.get(f"{API}/{path}", headers=headers).status_code == 403, path
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
    # The asset page leaves out the parts that belong to hidden sections instead of showing them empty
    shown = client.get(f"{API}/assets/{asset['id']}", headers=headers).json()
    assert shown["documents"] is None and shown["recent_breakdowns"] is None and shown["work_orders"] is None
    assert shown["breakdown_summary"] is None
    assert client.get(f"{API}/assets/{asset['id']}", headers=factory.admin).json()["recent_breakdowns"]

    # Without the Assets section a user can still name a machine in a form, and learns nothing else about it
    _, asker = person(client, factory, "viewer", ["chat.ask"])
    assert client.get(f"{API}/assets", headers=asker).status_code == 403
    assert client.get(f"{API}/assets/options", headers=asker).json() == [
        {"id": asset["id"], "asset_code": "CNC-01", "name": "Machine CNC-01"}
    ]


def test_approval_can_be_given_to_one_technician_and_taken_from_a_manager(client, factory):
    asset = factory.asset("CNC-01")
    _, author = person(client, factory, "technician")
    _, approver = person(client, factory, "technician", [*role_permissions("technician"), "work_orders.approve"])
    manager, manager_headers = person(client, factory, "maintenance_manager")
    without_approval = [p for p in role_permissions("maintenance_manager") if p != "work_orders.approve"]
    assert set_access(client, factory, manager["id"], without_approval).json()["custom_permissions"] is True

    order = manual_order(client, author, asset["id"])
    move(client, author, order["id"], "pending_approval")
    refused = move(client, manager_headers, order["id"], "approved")
    assert refused.status_code == 403 and "Approve, reject and cancel work orders" in refused.json()["detail"]
    seen = client.get(f"{API}/work-orders/{order['id']}", headers=manager_headers).json()
    assert seen["allowed_transitions"] == []
    assert client.get(f"{API}/work-orders/{order['id']}", headers=approver).json()["allowed_transitions"] == [
        "approved", "rejected", "cancelled"
    ]
    approved = move(client, approver, order["id"], "approved")
    assert approved.status_code == 200 and approved.json()["approved_by_name"] == "alpha technician"

    # Approval access does not lift the four-eyes rule
    own = manual_order(client, approver, asset["id"])
    move(client, approver, own["id"], "pending_approval")
    assert move(client, approver, own["id"], "approved").status_code == 403


def test_each_work_order_step_needs_its_own_permission(client, factory):
    asset = factory.asset("CNC-01")
    _, reader = person(client, factory, "technician", ["work_orders.view"])
    _, drafter = person(client, factory, "viewer", ["work_orders.draft"])
    _, doer = person(client, factory, "viewer", ["work_orders.view", "work_orders.execute"])
    body = {"asset_id": asset["id"], "title": "Replace filter"}
    assert client.post(f"{API}/work-orders", headers=reader, json=body).status_code == 403
    assert client.post(f"{API}/work-orders", headers=doer, json=body).status_code == 403

    order = manual_order(client, drafter, asset["id"])
    assert move(client, doer, order["id"], "pending_approval").status_code == 403
    assert move(client, drafter, order["id"], "pending_approval").status_code == 200
    assert move(client, factory.admin, order["id"], "approved").status_code == 200
    assert move(client, drafter, order["id"], "in_progress").status_code == 403
    assert move(client, doer, order["id"], "in_progress").status_code == 200
    assert move(client, doer, order["id"], "completed").status_code == 200


def test_actions_follow_the_chosen_access(client, factory):
    asset = factory.asset("CNC-01")
    # A viewer who may report breakdowns but not see documents; a manager who may no longer manage assets
    _, reporter = person(client, factory, "viewer", ["breakdowns.report"])
    breakdown = {"asset_id": asset["id"], "reported_at": "2026-03-01T08:00:00Z", "symptoms": "Machine stopped"}
    assert client.post(f"{API}/breakdowns", headers=reporter, json=breakdown).status_code == 201
    assert client.get(f"{API}/breakdowns", headers=reporter).status_code == 200  # the action made its section visible
    assert client.get(f"{API}/documents", headers=reporter).status_code == 403
    assert client.post(f"{API}/chat", headers=reporter, json={"question": "What is the oil level?"}).status_code == 403

    manager, headers = person(client, factory, "maintenance_manager")
    limited = [p for p in role_permissions("maintenance_manager") if p not in ("assets.manage", "audit.view")]
    set_access(client, factory, manager["id"], limited)
    assert client.post(f"{API}/assets", headers=headers, json={"asset_code": "P-1", "name": "Press"}).status_code == 403
    assert client.get(f"{API}/audit", headers=headers).status_code == 403
    assert client.get(f"{API}/chat/unanswered", headers=headers).status_code == 200


def test_changing_access_is_checked_recorded_and_reversible(client, factory):
    user, headers = person(client, factory, "technician")
    assert set_access(client, factory, user["id"], ["made.up"]).status_code == 422
    assert set_access(client, factory, user["id"], ["users.manage"]).status_code == 422  # never handed out
    assert client.patch(f"{API}/users/{user['id']}", headers=headers, json={"permissions": list(PERMISSIONS)}).status_code == 403

    changed = set_access(client, factory, user["id"], ["documents.manage"]).json()
    assert changed["permissions"] == ["documents.view", "documents.manage"] and changed["custom_permissions"] is True
    # It applies to the login the user already has
    assert client.get(f"{API}/work-orders", headers=headers).status_code == 403
    event = client.get(f"{API}/audit", headers=factory.admin, params={"resource_type": "user"}).json()["items"][0]
    assert event["action"] == "user.update" and event["detail"] == "permissions: documents.view, documents.manage"

    nothing = set_access(client, factory, user["id"], []).json()
    assert nothing["permissions"] == [] and nothing["custom_permissions"] is True
    assert client.get(f"{API}/dashboard", headers=headers).status_code == 403
    assert client.get(f"{API}/auth/me", headers=headers).status_code == 200

    back = set_access(client, factory, user["id"], None).json()
    assert back["custom_permissions"] is False and back["permissions"] == role_permissions("technician")

    # A new role starts from its own standard; an administrator cannot be limited
    set_access(client, factory, user["id"], ["chat.ask"])
    promoted = client.patch(f"{API}/users/{user['id']}", headers=factory.admin, json={"role": "maintenance_manager"}).json()
    assert promoted["custom_permissions"] is False and promoted["permissions"] == role_permissions("maintenance_manager")
    client.patch(f"{API}/users/{user['id']}", headers=factory.admin, json={"role": "admin"})
    assert set_access(client, factory, user["id"], ["chat.ask"]).status_code == 422
    assert "users.manage" in client.get(f"{API}/auth/me", headers=headers).json()["permissions"]


def test_closing_a_conflict_follows_the_setting_and_the_chosen_access(client, factory, monkeypatch):
    assert "conflicts.resolve" in role_permissions("maintenance_manager")
    monkeypatch.setattr("backend.app.core.config.settings.CONFLICT_RESOLVE_ROLE", "admin")
    assert "conflicts.resolve" not in role_permissions("maintenance_manager")
    # Chosen for one technician, it holds whatever the setting says for the roles
    user, _ = person(client, factory, "technician", ["conflicts.resolve"])
    assert user["permissions"] == ["conflicts.view", "conflicts.resolve"]


def test_the_administrator_approves_alone_and_can_let_others_do_so(client, factory):
    asset = factory.asset("CNC-01")
    assert "work_orders.approve_own" not in role_permissions("maintenance_manager")
    own = manual_order(client, factory.admin, asset["id"])
    move(client, factory.admin, own["id"], "pending_approval")
    assert "approved" in client.get(f"{API}/work-orders/{own['id']}", headers=factory.admin).json()["allowed_transitions"]
    assert move(client, factory.admin, own["id"], "approved").status_code == 200
    event = client.get(f"{API}/audit", headers=factory.admin, params={"resource_type": "work_order"}).json()["items"][0]
    assert event["detail"] == "pending_approval -> approved (approved by its author)"

    # A manager still needs a second person, until the administrator gives this one manager the access
    manager, headers = person(client, factory, "maintenance_manager")
    order = manual_order(client, headers, asset["id"])
    move(client, headers, order["id"], "pending_approval")
    refused = move(client, headers, order["id"], "approved")
    assert refused.status_code == 403 and "administrator" in refused.json()["detail"]
    # Ticked on its own, it brings the approval access it depends on
    alone = set_access(client, factory, manager["id"], ["work_orders.approve_own"]).json()["permissions"]
    assert alone == ["work_orders.view", "work_orders.approve", "work_orders.approve_own"]
    set_access(client, factory, manager["id"], [*role_permissions("maintenance_manager"), "work_orders.approve_own"])
    assert move(client, headers, order["id"], "approved").status_code == 200
