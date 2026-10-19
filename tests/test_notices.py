import pytest
from schoolbridge.notices import validate_draft
from schoolbridge.notices import validate_analysis


def test_valid():
    s, a = validate_analysis(
        {"summary": "Field trip on Friday", "actions": [{"task": "Sign the form", "due": "2026-10-23"}]}
    )
    assert s == "Field trip on Friday"
    assert a == [{"task": "Sign the form", "due": "2026-10-23"}]


def test_bad_due_becomes_none():
    _, a = validate_analysis({"summary": "x", "actions": [{"task": "Pay", "due": "tomorrow"}]})
    assert a[0]["due"] is None


def test_missing_summary_rejected():
    with pytest.raises(ValueError):
        validate_analysis({"actions": []})


def test_not_a_dict_rejected():
    with pytest.raises(ValueError):
        validate_analysis(["nope"])


def test_junk_actions_skipped_and_capped():
    data = {"summary": "x", "actions": ["bad", {"task": ""}] + [{"task": f"t{i}"} for i in range(20)]}
    _, a = validate_analysis(data)
    assert len(a) == 10

def test_draft_valid():
    d, b = validate_draft({"draft": "Hello", "back_translation": "Привет"})
    assert d == "Hello" and b == "Привет"


def test_draft_missing_parts_rejected():
    with pytest.raises(ValueError):
        validate_draft({"draft": "Hello"})
    with pytest.raises(ValueError):
        validate_draft({"back_translation": "x"})