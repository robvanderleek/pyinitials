from pyinitials import initials


def test_all():
    assert initials('John Doe') == 'JD'
