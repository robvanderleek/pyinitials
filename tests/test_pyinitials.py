from pyinitials import initials
from pyinitials.pyinitials import _preferred_initials, _is_uppercase_only, _is_email_address, \
    _get_all_initials_for_word, _combine_all, _get_all_initials_for_name


def test_initials():
    assert initials('John Doe') == 'JD'
    assert initials('john doe') == 'jd';
    assert initials('John Doe <joe@example.com>') == 'JD'
    assert initials('joe@example.com') == 'jo'
    assert initials('John Doe (dj)') == 'dj'
    assert initials('안형준') == '안형'


def test_preferred_initials():
    assert _preferred_initials('John Doe (dj)') == 'dj'


def test_is_uppercase_only():
    assert _is_uppercase_only('JD') is True
    assert _is_uppercase_only('Jd') is False


def test_is_email_pattern():
    assert _is_email_address('robvanderleek@gmail.com') is True
    assert _is_email_address('  robvanderleek@gmail.com') is True
    assert _is_email_address('robvanderleek@gmail.com  ') is True


def test_get_all_initials_for_word():
    assert _get_all_initials_for_word('rob') == ['r', 'ro', 'rob']


def test_combine_all():
    l = [['r', 'ro'], ['l', 'le']]
    assert _combine_all(l) == ['rl', 'rle', 'rol', 'role']


def test_get_all_initials_for_name():
    result = _get_all_initials_for_name('John Doe')
    expected = ['JD', 'JDo', 'JDoe', 'JoDoe', 'JohDoe', 'JohnDoe']
    assert result == expected
