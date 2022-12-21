import re
from typing import Any, Iterator, List, Callable


def filter_query(param: str, data: list[str]) -> list[str]:
    """Search (filter) for given param in data"""
    return list(filter(lambda row: param in row, data))


def regex_query(param: str, data: list[str]) -> list[str]:
    pattern: re.Pattern = re.compile(param)
    return list(filter(lambda x: re.search(pattern, x), data))


def map_query(param: str, data: list[str]) -> list[str]:
    col_number = int(param)
    return list(map(lambda row: row.split(' ')[col_number], data))


def unique_query(data: list[str], *args: Any, **kwargs: Any) -> list[str]:
    result = []
    seen = set()
    for row in data:
        if row in seen:
            continue
        else:
            result.append(row)
            seen.add(row)
    return result


def sort_query(param: str, data: list[str]) -> list[str]:
    reverse = False if param == 'asc' else True
    return sorted(data, reverse=reverse)


def limit_query(param: str, data: list[str]) -> list[str]:
    limit = int(param)
    return data[:limit]


CMD_TO_FUNCTION: dict[str, Callable] = {
    'filter': filter_query,
    'map': map_query,
    'unique': unique_query,
    'sort': sort_query,
    'limit': limit_query,
    'regex': regex_query,
}


def build_query(cmd: str, param: str, filename: str, data: Any = None) -> List[str]:
    if not data:
        with open(f'data/{filename}') as file:
            data = list(map(lambda row: row.strip(), file))
    return CMD_TO_FUNCTION[cmd](param=param, data=data)
