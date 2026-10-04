"""Cheap checks of the benchmark case data; they do not call Ollama.

The agent itself is measured by the benchmark, not by pytest:

    uv run python -m benchmark.run
"""
import copy

from benchmark.cases import CASES, compare, read_instructions


def test_every_instruction_has_expected_result():
    assert set(read_instructions()) == set(CASES)


def expected_as_result(expected):
    return {"status": "complete", "units": "mm",
            "outline": copy.deepcopy(expected["outline"]),
            "holes": copy.deepcopy(expected["holes"])}


def test_compare_accepts_expected_geometry():
    for expected in CASES.values():
        result = expected_as_result(expected)
        result["holes"].reverse()  # hole order does not matter
        assert compare(result, expected) == []


def test_compare_reports_differences():
    expected = next(iter(CASES.values()))
    result = expected_as_result(expected)
    result["outline"]["side"] += 5
    result["holes"][0]["diameter"] += 1
    problems = compare(result, expected)
    assert any("outline.side" in p for p in problems)
    assert any("hole diameter" in p for p in problems)


def test_compare_reports_incomplete_status():
    expected = next(iter(CASES.values()))
    assert compare({"status": "incomplete", "missing": ["side"]}, expected)
