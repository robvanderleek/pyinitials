from pyinitials import initials, Candidate
from pyinitials.pyinitials import _preferred_initials, _is_uppercase_only, _is_email_address, \
    _get_all_initials_for_word, _combine_all, _get_all_initials_for_name, find, _clear_all_non_characters


def test_has_function():
    assert callable(initials)
    # t.is(typeof initials.addTo, 'function', 'has method initials.addTo')
    # t.is(typeof initials.parse, 'function', 'has method initials.parse')
    assert callable(find)


def test_initials():
    assert initials('John Doe') == 'JD'
    assert initials('john doe') == 'jd'
    assert initials('John Doe <joe@example.com>') == 'JD'
    assert initials('joe@example.com') == 'jo'
    assert initials('John Doe (dj)') == 'dj'
    assert initials('안형준') == '안형'


def test_initials_with_length():
    assert initials('John Doe', 3) == 'JDo'
    assert initials('John D.', 3) == 'JoD'


def test_initials_with_array():
    assert initials(['John Doe', 'Robert Roe', 'Larry Loe']) == ['JD', 'RR', 'LL']
    assert initials(['John Doe', 'Jane Dane']) == ['JDo', 'JDa']
    assert initials(['John Doe (JD)', 'Jane Dane']) == ['JD', 'JDa']
    assert initials(['John Doe', 'Jane Dane', 'John Doe']) == ['JDo', 'JDa', 'JDo']
    assert initials(['John Smith', 'Jane Smith']) == ['JSm', 'JaS']
    assert initials(['John Doe (JoDo)', 'Jane Dane']) == ['JoDo', 'JD']
    assert initials(['John Doe (JoDo)', 'Jane Dane (JoDo)']) == ['JoDo', 'JoDo']

# t.deepEqual(initials(['John Doe (JD)', 'Jane Dane']), ['JD', 'JDa'], 'preferred initials are respected in other names: John Doe (JD), Jane Dane ☛ JD, JDa')
# t.deepEqual(initials(['John Doe <joe@example.com>']), ['JD'], 'emails are ignored in arrays')
# t.deepEqual(initials(['joe@example.com']), ['jo'], 'domains are ignored when a name is an email')
#
# // https://github.com/gr2m/initials/issues/1
# t.deepEqual(initials(['j']), ['j'], 'j ☛ j')
#
# // https://github.com/gr2m/initials/issues/14
# t.deepEqual(initials(['Moe Minutes', 'Moe Min']).sort(), ['MMi', 'MoM'], '["Moe Minutes", "Moe Min"] ☛ ["MoM", "MMi"]')


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

    assert result[2][0].value == 'JD'
    assert result[3][0].value == 'JDo'
    assert result[4][0].value == 'JDoe'
    assert result[5][0].value == 'JoDoe'
    assert result[6][0].value == 'JohDoe'
    assert result[7][0].value == 'JohnDoe'


def test_clear_all_non_characters():
    assert _clear_all_non_characters('abc') == 'abc'
    assert _clear_all_non_characters('John D.') == 'John D'


def test_candidate():
    c1 = Candidate('aap', False, False)
    c2 = Candidate('aap', False, False)
    c3 = Candidate('aap', True, False)
    c4 = Candidate('noot', False, False)

    assert c1 == c2
    assert c2 == c3
    assert c1 == c3
    assert c1 != c4