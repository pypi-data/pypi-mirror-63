import json
from functools import reduce
import operator
from typing import Iterable, Any


def load_data(path: str) -> list:
    return json.load(open(path, 'r', encoding='utf8'))


def get_by_path(root: dict, items: Iterable) -> Any:
    # courtesy: https://stackoverflow.com/a/14692747/5538961
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def get_issue_type(issue: dict) -> str:
    return get_by_path(issue, ('fields', 'issuetype', 'name'))


def get_reference(issue):
    return issue['key']


def get_title(issue):
    return get_by_path(issue, ('fields', 'summary'))


def get_labels(issue) -> list:
    return get_by_path(issue, ('fields', 'labels'))


def get_description(issue):
    return get_by_path(issue, ('fields', 'description'))


def get_status(issue) -> str:
    return get_by_path(issue, ('fields', 'status', 'name'))


def get_priority(issue) -> str:
    return get_by_path(issue, ('fields', 'priority', 'name'))


def get_date_created(issue) -> str:
    return get_by_path(issue, ('fields', 'created'))


def get_date_updated(issue) -> str:
    return get_by_path(issue, ('fields', 'updated'))


def filter_epics(issues: list) -> list:
    return [issue for issue in issues if get_issue_type(issue) == 'Epic']


def get_jiradata(issue: dict) -> dict:
    return {
        'ref': get_reference(issue),
        'status': get_status(issue),
        'priority': get_priority(issue),
        'issue_type': get_issue_type(issue),
        'date_update': get_date_updated(issue),
        'date_created': get_date_created(issue),
        'title': get_title(issue),
        'description': get_description(issue),
        'labels': get_labels(issue)
    }
