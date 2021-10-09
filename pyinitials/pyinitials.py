import re
from dataclasses import dataclass
from functools import cmp_to_key
from typing import Union


def initials(s: Union[str, list] = None, length=2, existing=None) -> Union[str, list]:
    if s is None:
        return ''
    if existing is None:
        existing = {}
    if type(s) == list:
        return _list_initials(s, length, existing)
    if s in existing:
        return existing[s]
    candidates = _get_candidates(s, length)
    return candidates[0].value


def find(s: str, length=2, existing=None) -> str:
    return initials(s, length, existing)


def add_to(i: Union[str, list] = None, length=2, existing=None) -> Union[str, list[str]]:
    if i is None:
        return ''
    if type(i) == list:
        result = []
        parts_list = parse(i, length, existing)
        for p in parts_list:
            result.append(_format(p))
        return result
    else:
        parts = parse(i, length, existing)
        return _format(parts)


@dataclass
class Parts:
    name: str
    initials: Union[str, None] = None
    email: str = None


def parse(i=None, length=2, existing=None) -> Union[Parts, list[Parts], None]:
    if i is None:
        return None
    elif type(i) == list:
        return _parse_multiple(i, length, existing)
    else:
        return _parse_single(i, length, existing)


def _parse_multiple(l: list[str], length: int, existing: dict) -> list[Parts]:
    initials_list = initials(l, length, existing)
    result = []
    for idx, s in enumerate(l):
        result.append(_parse_single(s, length, {s: initials_list[idx]}))
    return result


def _parse_single(s: str, length: int, existing: dict) -> Parts:
    initials_part = initials(s, length, existing)
    email = _get_email_address(s)
    name_part = _remove_email_address(_remove_preferred_initials(s))
    if _is_email_address(name_part):
        name = name_part.strip()
    else:
        name = _clear_all_non_characters(name_part).strip()
    if name == initials_part and not _has_preferred_initials(s):
        return Parts(name, None, email)
    else:
        return Parts(name, initials_part, email)


def _format(parts: Parts):
    if not parts.initials and not parts.email:
        return parts.name
    if not parts.email:
        return parts.name + ' (' + parts.initials + ')'
    if not parts.name or (parts.name == parts.email):
        return parts.email + ' (' + parts.initials + ')'
    return parts.name + ' (' + parts.initials + ') <' + parts.email + '>'


@dataclass
class Candidate:
    value: str
    preferred: bool = False
    cached: bool = False

    def __eq__(self, othr):
        return isinstance(othr, type(self)) and self.value == othr.value

    def __hash__(self):
        return hash((self.value, self.preferred, self.cached))


def _get_candidates_by_length(candidates: dict[int, list[Candidate]], length: int) -> list[Candidate]:
    sorted_keys = sorted(candidates.keys())
    if len(sorted_keys) == 1:
        return candidates[sorted_keys[0]]

    for k in sorted_keys:
        if k >= length:
            return candidates[k]

    return candidates[sorted_keys[-1]]


def _get_candidates(s: str, length=2) -> list[Candidate]:
    if _is_uppercase_only(s):
        return [Candidate(s)]
    preferred = _get_preferred_initials(s)
    if preferred:
        return [Candidate(preferred, True)]
    s = _remove_email_address(s)
    if _is_email_address(s):
        s = re.sub(r'@\S+[.]\S+', '', s)
    s = _clear_all_non_characters(s)
    first_letters = [w[0] for w in re.findall(r'\w+', s)]
    result = ''.join(first_letters)
    if len(result) >= length:
        return [Candidate(result)]
    else:
        all_initials = _get_all_initials_for_name(s)
        return _get_candidates_by_length(all_initials, length)


def _list_initials(string_list: list[str], length, existing) -> list[str]:
    result = []
    cache_map = {}
    for n in string_list:
        if len(n) == 0 or n.isspace():
            result.append(Candidate(''))
            continue
        if n in cache_map:
            cached = cache_map[n]
            result.append(Candidate(cached.value, cached.preferred, True))
            continue
        if n in existing:
            result.append(Candidate(existing[n]))
            continue
        candidates = _get_candidates(n, length)
        for c in candidates:
            if c.preferred:
                result.append(c)
                cache_map[n] = c
                break
            if c in result:
                continue
            result.append(c)
            cache_map[n] = c
            break
        else:
            return _list_initials(string_list, length + 1, existing)
    return [c.value for c in result]


def _get_all_initials_for_name(n: str) -> dict[int, list[Candidate]]:
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
            (result[len(s)]).append(Candidate(s))
        else:
            result[len(s)] = [Candidate(s)]

    return result


def _is_uppercase_only(fullname: str):
    uppercase_letters_only_pattern = '^[A-Z]+$'
    return re.match(uppercase_letters_only_pattern, fullname) is not None


PREFERRED_PATTERN = r'[(]([^[)]+)[)]'


def _get_preferred_initials(s: str) -> str:
    match = re.search(PREFERRED_PATTERN, s)
    if match:
        return match.group(1)


def _has_preferred_initials(s: str) -> bool:
    return _get_preferred_initials(s) is not None


def _remove_preferred_initials(s: str) -> str:
    return re.sub(PREFERRED_PATTERN, '', s)


EMAIL_PATTERN = r'\S+@\S+[.]\S+'


def _get_email_address(s: str) -> Union[None, str]:
    match = re.search(EMAIL_PATTERN, s)
    if match:
        result = match.group()
        result = result.lstrip('<')
        result = result.rstrip('>')
        return result


def _is_email_address(s: str) -> bool:
    return re.match(rf'^\s*{EMAIL_PATTERN}\s*$', s) is not None


def _remove_email_address(s: str) -> str:
    stripped = re.sub(f'[<]{EMAIL_PATTERN}[>]', '', s)
    matches = list(re.finditer(EMAIL_PATTERN, s))
    if len(matches) > 0:
        m = matches.pop()
        stripped_again = s[0:m.span()[0]] + s[m.span()[1]:]
        if len(stripped_again) > 0 and not stripped_again.isspace():
            return stripped_again
    return stripped


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
