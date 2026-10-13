"""The frontend draws only the page the user is on (frontend/js/latest.js); its tests run in Node."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_page_drawing_order():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not installed; run: node --test frontend/tests")
    run = subprocess.run(
        [node, "--test", str(ROOT / "frontend" / "tests" / "latest.test.js")], capture_output=True, text=True, timeout=120,
    )
    assert run.returncode == 0, run.stdout + run.stderr


def test_scripts_are_revalidated_after_a_deployment(client):
    first = client.get("/static/js/app.js")
    assert first.status_code == 200 and first.headers["cache-control"] == "no-cache"
    again = client.get("/static/js/app.js", headers={"If-None-Match": first.headers["etag"]})
    assert again.status_code == 304 and again.headers["cache-control"] == "no-cache"


def test_application_loads_the_helper_before_it_is_used():
    html = (ROOT / "frontend" / "app.html").read_text(encoding="utf-8")
    assert 0 < html.find("/static/js/latest.js") < html.find("/static/js/app.js")
