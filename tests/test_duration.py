from pwdgenerator.duration import Duration

def test_minutes():
    assert Duration(minutes=30).inMinutes == 30
    assert Duration(minutes=30).inHours == 0.5
    assert Duration(minutes=1440).inDays == 1
    assert Duration(minutes=10080).inWeeks == 1

def test_hours():
    assert Duration(hours=1).inMinutes == 60
    assert Duration(hours=12).inHours == 12
    assert Duration(hours=24).inDays == 1
    assert Duration(hours=168).inWeeks == 1

def test_days():
    assert Duration(days=1).inMinutes == 1440
    assert Duration(days=1).inHours == 24
    assert Duration(days=31).inDays == 31
    assert Duration(days=14).inWeeks == 2
    