#!/usr/bin/env python3
"""Small integrity check for the packaged static presentation."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
html = (HERE / "index.html").read_text()
payload = (HERE / "artifact-manifest.js").read_text()
manifest = json.loads(
    payload.removeprefix("window.TC2_ARTIFACT_MANIFEST=").removesuffix(";\n")
)

assert (HERE / "index.html").is_file()
assert 'data-choice="versions"' in html
assert 'data-choice="leakage"' in html
assert 'data-choice="example-versions"' in html
assert 'data-choice-value="v0"' in html and html.count(">개선 사례</button>") == 3 and html.count(">실패 사례</button>") == 3
assert 'id="log-version"' in html and 'id="log-roles"' in html
assert html.count('data-log-role=') == 3
assert "버전별 핵심 차이" in html and "Research Question" in html
assert html.index("<h2>v3 exploration coverage</h2>") < html.index("<h2>Leakage run</h2>")
assert "data-highlight=" in html and "log-stats" not in html
assert len(manifest["runs"]) == 12
assert len([item for item in manifest["items"] if item["kind"] == "prompt"]) == 703
assert all((HERE / item["path"]).is_file() for item in manifest["items"])
assert {
    run["run"]: run["solved"] for run in manifest["runs"]
} == {
    "v1-original-42": 1,
    "v1-original-43": 7,
    "v1-random_chars-42": 0,
    "v1-random_chars-43": 8,
    "v2-original-42": 8,
    "v2-original-43": 5,
    "v2-random_chars-42": 8,
    "v2-random_chars-43": 0,
    "v3-original-42": 8,
    "v3-original-43": 8,
    "v3-random_chars-42": 0,
    "v3-random_chars-43": 1,
}

print(f"OK: {len(manifest['runs'])} runs, {len(manifest['items'])} indexed files")
