"""Cheap checks of the benchmark case data; they do not call Ollama.

The agent itself is measured by the benchmark, not by pytest:

    uv run python -m benchmark.run
"""
import copy

from benchmark.cases_2d import CASES, compare
from benchmark.cases_3d import CASES as CASES_3D


def test_cases_are_well_formed():
    for cases in (CASES, CASES_3D):
        instructions = [case["instruction"] for case in cases]
        assert len(instructions) == len(set(instructions)), "duplicate instruction"
        for case in cases:
            assert case["section"] in ("Full information", "Partial information")
    for case in CASES:
        assert set(case["expected"]) == {"outline", "holes"}


def expected_as_result(expected):
    return {"status": "complete", "units": "mm",
            "outline": copy.deepcopy(expected["outline"]),
            "holes": copy.deepcopy(expected["holes"])}


def test_compare_accepts_expected_geometry():
    for expected in (case["expected"] for case in CASES):
        result = expected_as_result(expected)
        result["holes"].reverse()  # hole order does not matter
        assert compare(result, expected) == []


def test_compare_reports_differences():
    expected = CASES[0]["expected"]
    result = expected_as_result(expected)
    result["outline"]["side"] += 5
    result["holes"][0]["diameter"] += 1
    problems = compare(result, expected)
    assert any("outline.side" in p for p in problems)
    assert any("hole diameter" in p for p in problems)


def test_compare_reports_incomplete_status():
    expected = CASES[0]["expected"]
    assert compare({"status": "incomplete", "missing": ["side"]}, expected)
