from datetime import timedelta

import pytest

from pwdgenerator import Duration


def test_minutes():
    assert Duration(minutes=30).total_minutes == 30
    assert Duration(minutes=30).total_hours == 0.5
    assert Duration(minutes=1440).total_days == 1
    assert Duration(minutes=10080).total_weeks == 1


def test_hours():
    assert Duration(hours=1).total_minutes == 60
    assert Duration(hours=12).total_hours == 12
    assert Duration(hours=24).total_days == 1
    assert Duration(hours=168).total_weeks == 1


def test_days():
    assert Duration(days=1).total_minutes == 1440
    assert Duration(days=1).total_hours == 24
    assert Duration(days=31).total_days == 31
    assert Duration(days=14).total_weeks == 2


def test_weeks():
    assert Duration(weeks=1).total_minutes == 10080
    assert Duration(weeks=1).total_hours == 168
    assert Duration(weeks=1).total_days == 7
    assert Duration(weeks=2).total_weeks == 2


def test_summary():
    assert Duration(minutes=1440, hours=24, days=1, weeks=1).total_days == 10


def test_is_a_timedelta():
    assert isinstance(Duration(days=1), timedelta)
    assert Duration(days=1) == timedelta(days=1)


@pytest.mark.parametrize('text, days', [
    ('2w', 14), ('10d', 10), ('12h', 0.5), ('1d12h', 1.5), ('1w 3d', 10),
    ('90min', 1 / 16), ('2 weeks', 14), ('1.5d', 1.5),
])
def test_parse(text, days):
    assert Duration.parse(text).total_days == pytest.approx(days)


@pytest.mark.parametrize('text', ['', 'week', '10', '10y', '0d', '2w!'])
def test_parse_errors(text):
    with pytest.raises(ValueError):
        Duration.parse(text)
