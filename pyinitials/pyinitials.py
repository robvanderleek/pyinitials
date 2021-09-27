import re
from functools import cmp_to_key, reduce
from typing import Union


def initials(s: Union[str, list], length=2, existing={}) -> str:
    if type(s) == list:
        return _list_initials(s, length, existing)
    all_options = _possible_initials(s, length)
    if len(all_options) == 1:
        return all_options[0]
    for o in all_options:
        if len(o) >= length:
            return o
    return all_options[-1]


def find(s: str) -> str:
    return initials(s)


def _possible_initials(s: str, length=2) -> list[str]:
    if _is_uppercase_only(s):
        return [s]
    preferred = _preferred_initials(s)
    if preferred:
        return [preferred]
    if _is_email_address(s):
        s = re.sub(r'@\S+[.]\S+', '', s)
    s = _remove_email_address(s)
    s = _clear_all_non_characters(s)
    first_letters = [w[0] for w in re.findall(r'\w+', s)]
    result = ''.join(first_letters)
    if len(result) >= length:
        return [result]
    else:
        return _get_all_initials_for_name(s)


def _list_initials(l: list, length, existing):
    result = []
    for n in l:
        result.append(initials(n, length, existing))
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

    def reduce_func(a, b):
        if len(a) == 0 or len(b) > len(a[-1]):
            return a + [b]
        else:
            return a

    return reduce(reduce_func, all_sorted, [])


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
