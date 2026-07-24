#!/usr/bin/env python3
"""Small integrity check for the packaged static presentation."""

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
html = (HERE / "index.html").read_text()
archive = (HERE.parent / "index.html").read_text()
payload = (HERE / "artifact-manifest.js").read_text()
manifest = json.loads(
    payload.removeprefix("window.TC2_ARTIFACT_MANIFEST=").removesuffix(";\n")
)

assert (HERE / "index.html").is_file()
assert '<a class="brand" href="../">260724</a>' in html and "TC2 / 260724" not in html
assert "<h1>NES VISUALIZATIONS</h1>" in archive
assert "<strong>High-level Abstraction w/o Domain Description</strong>" in archive
assert all(
    text not in archive
    for text in (
        "연구 발표 아카이브",
        "실험 결과와 분석 자료를 날짜별로 모았습니다.",
        "NES research visualizations",
        "TC2 High-level Abstraction",
    )
)
assert 'data-choice="versions"' in html
assert html.count('data-choice-panel="versions"') == 4
assert 'A["Transition 없이<br/>[Domain description] · Goal · Action · State<br/>Neutral few-shot example"]' in html
assert 'data-choice="leakage"' in html
assert 'data-choice="example-versions"' in html
assert 'data-choice-value="v0"' in html and html.count(">개선 사례</button>") == 2 and html.count(">실패 사례</button>") == 2
assert 'id="log-version"' in html and 'id="log-roles"' in html
assert html.count('data-log-role=') == 3
overview = html[html.index('id="versions"'):html.index('id="results"')]
assert '<a href="#versions">Overview</a>' in html and '<a href="#versions">버전</a>' not in html
assert '<p class="overview-heading"><strong>Recap:</strong></p>' in overview
assert "long-horizon planning이 domain knowledge 부족 문제가 두드러지는 과업 조건이다." in overview
assert "기존 연구, 문제 설정을 고려할 때 online, non-demo 세팅으로 가야한다." in overview
assert "Research Question: domain knowledge가 없음 + online learning setting에서 high-level을 어떻게 복원할까?" in overview
assert overview.count('class="overview-heading"') == 3 and ".overview-heading { font-size: 18px; }" in html
assert overview.index('aria-label="버전별 research question"') < overview.index('class="overview-heading">버전별 핵심 차이</h1>') < overview.index('data-choice="versions"')
assert "Revision trigger" in html and ">Trigger<" not in html
assert "구체적 예시" not in html and "<h1>버전별 주요 사례</h1>" in html
assert (
    html.index('href="#examples"')
    < html.index('href="#random-chars"')
    < html.index('href="#templates"')
    < html.index('href="#log"')
)
assert html.index("<h2>v3 exploration coverage</h2>") < html.index("<h2>Leakage run</h2>")
assert 'aria-label="버전별 solve rate"' not in html and "<th>전략</th>" not in html
assert "# generated response" not in html and "# Generated WM · verbatim excerpt" not in html
assert "data-highlight=" in html and html.count('class="leak-highlight"') >= 20 and "log-stats" not in html
assert html.count('<pre class="inline-viewer" data-canonicalize') == 3 and 'id="log-name-map" hidden' in html
assert 'nameMap.hidden = state.benchmark !== "random_chars"' in html
assert "PDDL grounding은 개선됐지만" not in html
assert "PDDL이 채집 가능한 <code>tree</code>를 하나만 있다고 작성해" in html
assert "타깃 level은 <code>make_stone_pickaxe</code>였지만, 탐색에서 관측한 achievement는 <code>ach_collect_wood</code>뿐이었다." in html
assert 'data-choice="examples-v3"' not in html
assert "성공 사례 · original · seed 43 · level 6 · candidate #1708" in html
name_map = dict(re.findall(r'<td data-canonical="([^"]+)">([^<]+)</td>', html))
assert len(name_map) == 22 and name_map["tree"] == "xcvkpr" and name_map["wood"] == "tpkhxk"
canonicalized = "place_zezroc inv_tpkhxk ach_place_zezroc make_tpkhxk_bcwrvm"
for canonical, random_name in name_map.items():
    canonicalized = canonicalized.replace(random_name, canonical)
assert canonicalized == "place_table inv_wood ach_place_table make_wood_pickaxe"
canonical_wm = (HERE / "artifacts/leakage/v2-random_chars-42-initial-response.txt").read_text()
for canonical, random_name in name_map.items():
    canonical_wm = canonical_wm.replace(random_name, canonical)
assert '"table": {"wood": 2}' in canonical_wm and '"wood": {"wood": 1}' in canonical_wm
examples = html[html.index('id="examples"'):html.index('id="random-chars"')]
assert all(name not in examples for name in ("xcvkpr", "tpkhxk", "zezroc"))
assert "candidate #479" not in examples
random_analysis = html[html.index('id="random-chars"'):html.index('id="templates"')]
assert "<h2>Exploration의 문제?</h2>" in random_analysis and "두 단계의 병목" not in random_analysis
assert "<h2>Causal identifiability 부족</h2>" in random_analysis
assert "<h2>지식의 공유 실패</h2>" in random_analysis
assert "candidate #427" in random_analysis and "candidate #495" in random_analysis and "candidate #479" in random_analysis
assert "동일 action의 성공과 no-op을 서로 다른 context에서 대조해야 한다." in random_analysis
assert "발견된 mechanics를 모듈 간에 공유해야 한다." in random_analysis
assert "mission과 관련 없어 보여도 다양하게 exploration 필요 &amp; clustered, abstracted 된 지식 필요 &amp; 이를 공유할 필요" in random_analysis
assert all(name not in random_analysis for name in name_map.values())
templates = html[html.index('id="templates"'):html.index("</main>")]
assert html.count("data-template-role=") == 3
assert all(
    f'data-choice="template-{role}"' in templates
    for role in ("scorer", "pddl", "wm")
)
assert "{}" not in templates
assert all(value == value.upper() for value in re.findall(r"\{([a-z_]+)\}", templates, re.I))
assert "Repair the scorer. The prior output failed validation with: {VALIDATION_ERROR}" in templates
assert all(
    placeholder in templates
    for placeholder in (
        "{MISSION}",
        "{PUBLIC_STATE_FORMAT}",
        "{PUBLIC_ACTIONS}",
        "{INITIAL_PUBLIC_STATE}",
        "{WARMUP_TRANSITIONS}",
        "{PREVIOUS_SCORER}",
        "{DOMAIN_DESCRIPTION}",
        "{RAW_STATE}",
        "{ACTION_SPACE}",
        "{OBSERVED_TRANSITIONS}",
        "{CURRENT_DOMAIN}",
        "{PREDICATE_ERROR}",
        "{PLANNER_ERROR}",
        "{PREDICTION_ERROR}",
        "{DOMAIN_FILE}",
        "{EXPECTED_PREDICATES}",
        "{PREDICATE_STUBS}",
        "{PROBLEM_FILE}",
        "{WORLD_MODEL}",
        "{GAME_DESCRIPTION}",
        "{CURRENT_STATE}",
        "{PREDICTION_ERRORS}",
    )
)
assert all(
    value in templates
    for value in (
        'data-choice-value="generate"',
        'data-choice-value="repair"',
        'data-choice-value="init"',
        'data-choice-value="revise"',
        'data-choice-value="transfer"',
        'data-choice-value="predicate"',
    )
)
assert all(value not in templates for value in ("seed 42", "seed 43", "make_stone_pickaxe"))
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
