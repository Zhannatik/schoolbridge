import pytest

from schoolbridge.assistant import parse_plan


def test_valid_plan():
    assert parse_plan('{"tool": "list_actions", "args": {}}') == ("list_actions", {})


def test_unknown_tool_becomes_none():
    assert parse_plan('{"tool": "delete_everything", "args": {}}')[0] == "none"


def test_bad_json_rejected():
    with pytest.raises(ValueError):
        parse_plan("not json")


def test_args_not_a_dict():
    assert parse_plan('{"tool": "add_child", "args": "x"}') == ("add_child", {})