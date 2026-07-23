#!/usr/bin/env python3
"""Package all TC2 runs for the static presentation."""

import json
import re
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] / "PyNES6"
RUNS = ROOT / "projects/tc/runs/exploration"
OUT = HERE / "artifacts"

SELECTED = {
    version: {"original": (42, 43), "random_chars": (42, 43)}
    for version in ("v1", "v2", "v3")
}
SUPPORTING = {
    "coverage/exploration_efficiency_c2000.json":
        ROOT / "projects/tc/runs/llm_beamsearch/exploration_efficiency_c2000.json",
    "leakage/v2-random_chars-42-initial-prompt.txt":
        RUNS / "v2-random_chars-42/worldmodel_events/wm_v1_init/prompt.txt",
    "leakage/v2-random_chars-42-initial-response.txt":
        RUNS / "v2-random_chars-42/worldmodel_events/wm_v1_init/response.txt",
    "leakage/v2-random_chars-42-results.json":
        RUNS / "v2-random_chars-42/results.json",
}

RUN_FILES = (
    "results.json",
    "run_config.json",
    "minicrafter_variant.json",
    "llm_calls.jsonl",
    "worldmodel.py",
    "validated_wm.py",
    "worldmodel_history.jsonl",
)
LEVEL_FILES = (
    "domain.pddl",
    "domain_at_entry.pddl",
    "validated_domain_at_entry.pddl",
    "problem.pddl",
    "predicates.py",
    "exploration_scorer.py",
    "wm_at_entry.py",
    "plan_log.jsonl",
    "scale_diagnostics.json",
    "trajectory.json",
)
PROMPT_RE = re.compile(r"call_(\d+)_(.+)_level_(\d+)\.txt$")


def prompt_meta(path):
    match = PROMPT_RE.match(path.name)
    if not match:
        return None
    label = match.group(2)
    if label == "exploration_scorer":
        role = "Exploration scorer"
    elif label.startswith("wm_"):
        role = "WM"
    else:
        role = "PDDL"
    stage = {
        "exploration_scorer": "init",
        "pddl_synth": "init",
        "pddl_revise": "revise",
        "pddl_transfer": "transfer",
        "predicate_synth": "predicate",
        "wm_synth": "init",
        "wm_revise": "revise",
    }.get(label, label)
    return int(match.group(3)), role, stage, "prompt"


def artifact_meta(relative):
    name = relative.name
    parts = relative.parts
    level = next(
        (int(part.removeprefix("level_")) for part in parts if part.startswith("level_")),
        -1,
    )
    if name == "exploration_scorer.py":
        return level, "Exploration scorer", "generated", "history"
    if "pddl_revise_events" in parts:
        kind = "prompt" if name.endswith("_prompt.txt") else "history"
        return level, "PDDL", "revise", kind
    if name.endswith(".pddl") or name == "predicates.py":
        stage = {
            "domain.pddl": "current",
            "domain_at_entry.pddl": "entry",
            "validated_domain_at_entry.pddl": "validated entry",
            "problem.pddl": "problem",
            "predicates.py": "predicate",
        }[name]
        return level, "PDDL", stage, "history"
    if "worldmodel_events" in parts:
        event = next(part for part in parts if part.startswith("wm_v"))
        stage = "init" if event.endswith("_init") else "revise"
        kind = "prompt" if name == "prompt.txt" else "history"
        return level, "WM", stage, kind
    if "worldmodel_history" in parts and name.startswith("wm_v"):
        return level, "WM", name.removesuffix(".py"), "history"
    if name in {"worldmodel.py", "validated_wm.py", "worldmodel_history.jsonl"}:
        return level, "WM", "final", "history"
    if name == "wm_at_entry.py":
        return level, "WM", "entry", "history"
    if name == "exploration_summary.json":
        return level, "Exploration scorer", "trace summary", "history"
    return level, "Run", "evidence", "history"


def wm_versions(run_dir):
    versions = {}
    for metadata_path in sorted((run_dir / "worldmodel_events").glob("wm_v*/metadata.json")):
        metadata = json.loads(metadata_path.read_text())
        prompt = Path(metadata.get("prompt_file", "")).name
        match = PROMPT_RE.match(prompt)
        if match:
            versions[metadata["version"]] = (int(match.group(3)), metadata["kind"])
    history = run_dir / "worldmodel_history.jsonl"
    last_level = 0
    if history.exists():
        for line in history.read_text().splitlines():
            row = json.loads(line)
            version = row["version"]
            if version in versions:
                last_level = versions[version][0]
            else:
                versions[version] = (last_level, row["kind"])
    return versions


def add_file(run_dir, source, destination, run_meta, items, wm_map):
    relative = source.relative_to(run_dir)
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    meta = prompt_meta(source) if relative.parts[0] == "llm_prompts" else artifact_meta(relative)
    if meta is None:
        meta = artifact_meta(relative)
    level, role, stage, kind = meta
    wm_match = next(
        (
            re.match(r"wm_v(\d+)", part)
            for part in relative.parts
            if re.match(r"wm_v(\d+)", part)
        ),
        None,
    )
    if role == "WM" and level == -1 and wm_match:
        version = int(wm_match.group(1))
        level, version_kind = wm_map.get(version, (-1, stage))
        if "worldmodel_history" in relative.parts:
            stage = f"v{version} {version_kind}"
    items.append(
        {
            **run_meta,
            "level": level,
            "role": role,
            "stage": stage,
            "kind": kind,
            "name": source.name,
            "path": target.relative_to(HERE).as_posix(),
            "source": relative.as_posix(),
            "bytes": source.stat().st_size,
        }
    )


def write_exploration_summary(run_dir, source, destination, run_meta, items):
    data = json.loads(source.read_text())
    candidates = data.get("candidates", [])
    signatures = [c.get("signature") or [] for c in candidates]
    state_hashes = {
        value
        for candidate in candidates
        for value in (candidate.get("context_hash"), candidate.get("after_hash"))
        if value
    }
    achievements = sorted(
        {
            token
            for signature in signatures
            for token in re.findall(r"\bach_[a-zA-Z0-9_]+", "\n".join(map(str, signature)))
        }
    )
    compact = {
        key: data.get(key)
        for key in (
            "schema_version",
            "strategy",
            "seed",
            "budget",
            "beam_width",
            "costs",
            "coverage",
            "scorer",
            "effect_first_seen",
            "later_plan_execution_revision_evidence_count",
            "wall_time_sec",
            "warmup_duration_sec",
        )
    }
    compact.update(
        {
            "candidate_count": len(candidates),
            "unique_state_count": len(state_hashes),
            "distinct_achievements": achievements,
            "selected_candidates": [
                {
                    key: candidate.get(key)
                    for key in ("index", "prefix", "action", "score", "signature")
                }
                for candidate in candidates
                if candidate.get("selected")
            ],
            "representatives": [
                {
                    key: representative.get(key)
                    for key in ("action", "delta", "score", "signature")
                }
                for representative in data.get("representatives", [])
            ],
        }
    )
    relative = source.relative_to(run_dir).parent / "exploration_summary.json"
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(compact, ensure_ascii=False, indent=2) + "\n")
    level, role, stage, kind = artifact_meta(relative)
    items.append(
        {
            **run_meta,
            "level": level,
            "role": role,
            "stage": stage,
            "kind": kind,
            "name": target.name,
            "path": target.relative_to(HERE).as_posix(),
            "source": source.relative_to(run_dir).as_posix(),
            "bytes": target.stat().st_size,
        }
    )


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    items = []
    runs = []

    for version, benchmarks in SELECTED.items():
        for benchmark, seeds in benchmarks.items():
            for seed in seeds:
                run_name = f"{version}-{benchmark}-{seed}"
                run_dir = RUNS / run_name
                destination = OUT / run_name
                run_meta = {
                    "version": version,
                    "benchmark": benchmark,
                    "seed": seed,
                    "run": run_name,
                }
                wm_map = wm_versions(run_dir)
                results = json.loads((run_dir / "results.json").read_text())
                levels = [
                    {"level": row["level_id"], "solved": row["solved"]}
                    for row in results["levels"]
                ]
                runs.append({**run_meta, "solved": sum(row["solved"] for row in levels), "levels": levels})

                for name in RUN_FILES:
                    source = run_dir / name
                    if source.exists():
                        add_file(run_dir, source, destination, run_meta, items, wm_map)
                for source in sorted((run_dir / "llm_prompts").glob("*.txt")):
                    add_file(run_dir, source, destination, run_meta, items, wm_map)
                for folder in ("worldmodel_history", "worldmodel_events"):
                    for source in sorted((run_dir / folder).rglob("*")):
                        if source.is_file() and source.suffix in {".py", ".txt", ".json"}:
                            add_file(run_dir, source, destination, run_meta, items, wm_map)
                for level in range(8):
                    level_dir = run_dir / f"level_{level}"
                    for name in LEVEL_FILES:
                        source = level_dir / name
                        if source.exists():
                            add_file(run_dir, source, destination, run_meta, items, wm_map)
                    for source in sorted((level_dir / "pddl_revise_events").glob("*")):
                        if source.is_file():
                            add_file(run_dir, source, destination, run_meta, items, wm_map)
                    exploration = level_dir / "exploration.json"
                    if exploration.exists():
                        write_exploration_summary(
                            run_dir, exploration, destination, run_meta, items
                        )

    manifest = {
        "selection": SELECTED,
        "runs": runs,
        "items": sorted(
            items,
            key=lambda item: (
                item["version"],
                item["benchmark"],
                item["seed"],
                item["level"],
                item["role"],
                item["stage"],
                item["name"],
            ),
        ),
    }
    payload = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))
    (HERE / "artifact-manifest.js").write_text(
        f"window.TC2_ARTIFACT_MANIFEST={payload};\n"
    )
    for relative, source in SUPPORTING.items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(f"Packaged {len(runs)} runs and {len(items)} indexed files in {OUT}")


if __name__ == "__main__":
    main()
