import re
from functools import cmp_to_key
from typing import Union


def initials(s: Union[str, list], length=2, existing=None) -> str:
    if existing is None:
        existing = {}
    if type(s) == list:
        return _list_initials(s, length, existing)
    possible_initials = _possible_initials(s, length)
    by_length = _select_length_from_possible_initials(possible_initials, length)
    return by_length[0]


def find(s: str) -> str:
    return initials(s)


def _select_length_from_possible_initials(possible_initials: dict[int, list[str]], length: int) -> list[str]:
    sorted_keys = sorted(possible_initials.keys())
    if len(sorted_keys) == 1:
        return possible_initials[sorted_keys[0]]

    for k in sorted_keys:
        if k >= length:
            return possible_initials[k]

    return possible_initials[sorted_keys[-1]]


def _possible_initials(s: str, length=2) -> dict[int, list[str]]:
    if _is_uppercase_only(s):
        return {len(s): [s]}
    preferred = _preferred_initials(s)
    if preferred:
        return {len(preferred): [preferred]}
    if _is_email_address(s):
        s = re.sub(r'@\S+[.]\S+', '', s)
    s = _remove_email_address(s)
    s = _clear_all_non_characters(s)
    first_letters = [w[0] for w in re.findall(r'\w+', s)]
    result = ''.join(first_letters)
    if len(result) >= length:
        return {len(result): [result]}
    else:
        return _get_all_initials_for_name(s)


def _list_initials(l: list, length, existing):
    result = []
    cache_map = {}
    for n in l:
        if n in cache_map:
            result.append(cache_map[n])
            continue
        possible_initials = _possible_initials(n, length)
        candidates = _select_length_from_possible_initials(possible_initials, length)
        for c in candidates:
            if c in result:
                continue
            result.append(c)
            cache_map[n] = c
            break
    if len(set(result)) != len(set(l)):
        return _list_initials(l, length + 1, existing)
    return result


def _get_all_initials_for_name(n: str):
    parts = re.compile(r'\s+').split(n)
    all_initials = [_get_all_initials_for_word(p) for p in parts]
    all_combined = _combine_all(all_initials)
    all_sorted = all_combined.copy()

    def compare_func(a, b):
        diff = len(a) - len(b)
        if diff == 0:
            return all_combined.index(a) - all_combined.index(b)
        else:
            return diff

    all_sorted.sort(key=cmp_to_key(compare_func))
    result = {}
    for s in all_sorted:
        if len(s) in result:
            (result[len(s)]).append(s)
        else:
            result[len(s)] = [s]

    return result


def _is_uppercase_only(fullname: str):
    uppercase_letters_only_pattern = '^[A-Z]+$'
    return re.match(uppercase_letters_only_pattern, fullname) is not None


def _preferred_initials(fullname: str):
    initials_in_name_pattern = '[(]([^[)]+)[)]'
    match = re.search(initials_in_name_pattern, fullname)
    if match:
        return match.group(1)


EMAIL_PATTERN = r'\S+@\S+[.]\S+'


def _is_email_address(s: str) -> bool:
    s = s.strip()
    return re.match(f'^{EMAIL_PATTERN}$', s) is not None


def _remove_email_address(s: str) -> str:
    return re.sub(EMAIL_PATTERN, '', s)


def _clear_all_non_characters(s: str) -> str:
    exp = re.compile(r"[\W\d_]", re.UNICODE)
    replaced = exp.sub(' ', s)
    return replaced.strip()


def _get_all_initials_for_word(s: str) -> list[str]:
    result = []
    for i in range(1, len(s) + 1):
        result.append(s[0:i])
    return result


def _combine_all(l: list):
    current = l.pop(0)
    results = []
    if len(l) > 0:
        next = _combine_all(l)
        for c in current:
            for n in next:
                results.append(c + n)
        return results
    else:
        return current
