#!/usr/bin/env python3
"""Small integrity check for the packaged static presentation."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
payload = (HERE / "artifact-manifest.js").read_text()
manifest = json.loads(
    payload.removeprefix("window.TC2_ARTIFACT_MANIFEST=").removesuffix(";\n")
)

assert (HERE / "index.html").is_file()
assert len(manifest["runs"]) == 9
assert len([item for item in manifest["items"] if item["source"].startswith("llm_prompts/")]) == 408
assert all((HERE / item["path"]).is_file() for item in manifest["items"])
assert {
    run["run"]: run["solved"] for run in manifest["runs"]
} == {
    "v1-original-42": 1,
    "v1-original-43": 7,
    "v1-random_chars-42": 0,
    "v2-original-42": 8,
    "v2-original-43": 5,
    "v2-random_chars-43": 0,
    "v3-original-42": 8,
    "v3-original-43": 8,
    "v3-random_chars-43": 1,
}

print(f"OK: {len(manifest['runs'])} runs, {len(manifest['items'])} indexed files")
