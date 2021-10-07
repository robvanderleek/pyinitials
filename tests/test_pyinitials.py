from pyinitials import initials, Candidate
from pyinitials.pyinitials import _get_preferred_initials, _is_uppercase_only, _is_email_address, \
    _get_all_initials_for_word, _combine_all, _get_all_initials_for_name, find, _clear_all_non_characters, Parts, \
    _format, add_to, _remove_email_address, parse


def test_has_function():
    assert callable(initials)
    assert callable(add_to)
    assert callable(parse)
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
    assert initials(['John Doe <joe@example.com>']) == ['JD']
    assert initials(['joe@example.com']) == ['jo']
    assert initials(['j']) == ['j']
    assert initials(['Moe Minutes', 'Moe Min']) == ['MMi', 'MoM']


def test_initials_with_existing():
    assert initials('John Doe',
                    existing={
                        'John Doe': 'JoDo'
                    }
                    ) == 'JoDo'
    assert initials(['John Doe', 'Jane Dane'],
                    existing={
                        'John Doe': 'JD'
                    }
                    ) == ['JD', 'JDa']


def test_add_to():
    assert add_to('John Doe') == 'John Doe (JD)'
    assert add_to('(JJ) Jack Johnson') == 'Jack Johnson (JJ)'
    assert add_to('JD') == 'JD'
    assert add_to('JD (JD)') == 'JD (JD)'
    assert add_to('John Doe (JoDo) joe@example.com') == 'John Doe (JoDo) <joe@example.com>'
    assert add_to('joe@example.com') == 'joe@example.com (jo)'
    assert add_to('joe (j)') == 'joe (j)', 'joe (j) ☛ joe (j)'
    assert add_to('Frönkää Üüd') == 'Frönkää Üüd (FÜ)'
    assert add_to('funky (fu)') == 'funky (fu)'
    assert add_to('test.test@test.org <test.test@test.org>') == 'test.test@test.org (tt)'


def test_add_to_with_array():
    assert add_to(['John Doe', 'Robert Roe', 'Larry Loe']) == ['John Doe (JD)', 'Robert Roe (RR)', 'Larry Loe (LL)']
    assert add_to(['John Doe', 'Jane Dane']) == ['John Doe (JDo)', 'Jane Dane (JDa)']


# test('initials.addTo(nameOrNames, {existing: initialsForNames})', function (t) {
#     t.equal(
#         initials.addTo('John Doe', {
#             existing: {
#                 'John Doe': 'JoDo'
#             }
#         }), 'John Doe (JoDo)', 'respect existing initials')
#
# t.deepEqual(
#     initials.addTo(['John Doe', 'Jane Dane'], {
#         existing: {
#             'John Doe': 'JD'
#         }
#     }), ['John Doe (JD)', 'Jane Dane (JDa)'], 'respect existing initials')
#
# t.end()
# })
#
def test_parse():
    assert parse('John Doe') == Parts('John Doe', 'JD')
    assert parse('JD') == Parts('JD')
    assert parse('joe@example.com') == Parts('joe@example.com', 'jo', 'joe@example.com')
    assert parse('John Doe <joe@example.com>') == Parts('John Doe', 'JD', 'joe@example.com')


#
# test('initials.parse(namesArray)', function (t) {
#     t.deepEqual(initials.parse(['John Doe', 'Robert Roe', 'Larry Loe']), [{ name: 'John Doe', initials: 'JD' }, { name: 'Robert Roe', initials: 'RR' }, { name: 'Larry Loe', initials: 'LL' }], 'John Doe, Robert Roe, Larry Loe ☛ name: John Doe, initials: JD; name: Robert Roe, initials: RR; name: Larry Loe, initials: LL')
#
# t.end()
# })
#
# test('initials.parse(nameOrNames, {existing: initialsForNames})', function (t) {
#     t.deepEqual(initials.parse('John Doe', {
#         existing: {
#             'John Doe': 'JoDo'
#         }
#     }), { name: 'John Doe', initials: 'JoDo' }, 'respect existing initials for single name')
#
# t.deepEqual(initials.parse(['John Doe', 'Jane Dane'], {
#     existing: {
#         'John Doe': 'JD'
#     }
# }), [{ name: 'John Doe', initials: 'JD' }, { name: 'Jane Dane', initials: 'JDa' }], 'respect existing initials  for multiple names')
#
# t.end()
# })
#
# test('initials(), no params', function (t) {
#     t.equal(initials(), '', 'initials() without nameOrNames, no initials')
# t.equal(initials.addTo(), '', 'initials.addTo() without nameOrNames, no initials')
# t.deepEqual(initials.parse(), {}, 'initials.parse() without nameOrNames, no initials')
#
# t.deepEqual(initials(['', '']), ['', ''], 'initials with multiple persons but no names')
#
# t.end()
# })
#
def test_name_is_less_than_3():
    assert initials('K') == 'K'
    assert initials('Mo') == 'Mo'


def test_preferred_initials():
    assert _get_preferred_initials('John Doe (dj)') == 'dj'


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


def test_format():
    assert _format(Parts("Jack Johnson", "JJ")) == "Jack Johnson (JJ)"
    assert _format(Parts("John Doe", "JD", "joe@example.com")) == "John Doe (JD) <joe@example.com>"


def test_remove_email_address():
    assert _remove_email_address('John Doe <joe@example.com>') == 'John Doe '
    assert _remove_email_address('test.test@test.org <test.test@test.org>') == 'test.test@test.org '
