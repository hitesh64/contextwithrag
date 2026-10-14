"""Create a demo factory with one user per role and the synthetic sample dataset.

    python -m backend.scripts.seed_demo [server URL, default http://127.0.0.1:8000]

The server must be running, on the same database as MONGO_URI in .env (the demo factory is marked
as paid there directly). Indexing uses embedding calls only, no text-generation quota.
The password of the four demo users is read from DEMO_PASSWORD in .env. The data is invented
sample data: do not show it to anyone as real factory records.
"""
import os
import sys

import httpx
from bson import ObjectId

from backend.app.core import config  # noqa: F401  (loads .env)
from backend.app.core.database import organizations
from backend.scripts import sample_loader

API = "/api/v1"
DOMAIN = "demo-factory.example.com"
TEAM = [("Meera Manager", "manager", "maintenance_manager"), ("Tarun Technician", "technician", "technician"), ("Vikram Viewer", "viewer", "viewer")]


def main() -> None:
    password = os.getenv("DEMO_PASSWORD", "")
    if len(password) < 8:
        sys.exit("Set DEMO_PASSWORD (at least 8 characters) in .env first; see .env.example.")
    admin_email = f"admin@{DOMAIN}"
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

    with httpx.Client(base_url=url, timeout=120) as client:
        try:
            created = client.post(f"{API}/auth/register", json={
                "organization_name": "Demo Factory (sample data)", "name": "Asha Admin", "email": admin_email, "password": password,
            })
        except httpx.ConnectError:
            sys.exit(f"No server at {url}. Start it first: uvicorn backend.app.main:app")
        if created.status_code == 409:
            sys.exit(f"The demo factory already exists (sign in as {admin_email}).")
        if created.status_code != 201:
            sys.exit(f"Could not create the demo factory: {created.text}")
        # The demo factory pays no registration fee
        organizations.update_one({"_id": ObjectId(created.json()["organization_id"])}, {"$set": {"status": "active"}})
        token = client.post(f"{API}/auth/login", json={"email": admin_email, "password": password}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        for name, prefix, role in TEAM:
            client.post(f"{API}/users", headers=headers, json={
                "name": name, "email": f"{prefix}@{DOMAIN}", "password": password, "role": role,
            }).raise_for_status()
        loaded = sample_loader.load(client, headers, strict=False)
        client.post(f"{API}/auth/logout", headers=headers)

    failed = {name: d["error"] for name, d in loaded["documents"].items() if d["status"] != "ready"}
    print(f"Demo factory created: {len(loaded['assets'])} assets, {len(loaded['documents'])} documents, breakdown log imported.")
    for name, error in failed.items():
        print(f"  NOT INDEXED: {name}: {error}")
    if failed:
        print("  Fix the cause, then use Reprocess on the Documents page.")
    print(f"Sign in as admin@, manager@, technician@ or viewer@{DOMAIN} with the DEMO_PASSWORD from .env.")


if __name__ == "__main__":
    main()
