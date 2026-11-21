import pytest

from pwdgenerator import Duration, Speed


def test_units():
    speed = Speed(15, per='minute')
    assert speed.per_minute == 15
    assert speed.per_hour == 900
    assert speed.per_day == 21600
    assert speed.per_week == 151200
    assert Speed(100, per='day').per_day == pytest.approx(100)


def test_period_as_duration():
    assert Speed(30, per=Duration(hours=1)) == Speed(0.5, per='minute')


def test_attempts_are_exact():
    # 15 a minute for two weeks
    assert Speed(15).attempts(Duration(weeks=2)) == 302400
    assert Speed(15) * Duration(weeks=2) == 302400
    assert Duration(weeks=2) * Speed(15) == 302400


@pytest.mark.parametrize('text, per_day', [
    ('15/min', 21600), ('100/day', 100), ('3/m', 4320), ('2 / h', 48), ('0.5/s', 43200),
])
def test_parse(text, per_day):
    assert Speed.parse(text).per_day == pytest.approx(per_day)


@pytest.mark.parametrize('text', ['15', '/min', 'abc/min', '15/year', '0/min', '-1/min'])
def test_parse_errors(text):
    with pytest.raises(ValueError):
        Speed.parse(text)
