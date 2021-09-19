import re
from functools import cmp_to_key, reduce


def initials(s: str) -> str:
    if _is_uppercase_only(s):
        return s
    preferred = _preferred_initials(s)
    if preferred:
        return preferred
    if _is_email_address(s):
        s = re.sub(r'@\S+[.]\S+', '', s)
    s = _remove_email_address(s)
    first_letters = [w[0] for w in re.findall(r'\w+', s)]
    result = ''.join(first_letters)
    if len(result) >= 2:
        return result
    else:
        all_options = _get_all_initials_for_name(s)
        for o in all_options:
            if len(o) >= 2:
                return o
        return all_options[-1]


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
