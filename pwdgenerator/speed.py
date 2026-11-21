from __future__ import annotations

from datetime import timedelta
from fractions import Fraction
from typing import Union

from pwdgenerator.duration import Duration

__all__ = ['Speed']

_PERIODS = {
    'second': Duration(seconds=1),
    'minute': Duration(minutes=1),
    'hour': Duration(hours=1),
    'day': Duration(days=1),
    'week': Duration(weeks=1),
}
_ALIASES = {
    's': 'second', 'sec': 'second', 'second': 'second',
    'm': 'minute', 'min': 'minute', 'minute': 'minute',
    'h': 'hour', 'hour': 'hour',
    'd': 'day', 'day': 'day',
    'w': 'week', 'week': 'week',
}


def exact(number: float) -> Fraction:
    """``0.1`` as the decimal number people mean, not its binary approximation."""
    return Fraction(number) if isinstance(number, (int, Fraction)) else Fraction(repr(float(number)))


def seconds(duration: timedelta) -> Fraction:
    return Fraction(duration // timedelta(microseconds=1), 1_000_000)


class Speed:
    """How many passwords an attacker can try per unit of time, the ``V``.

    >>> Speed(15, per='minute').per_day
    21600.0
    """

    def __init__(self, count: float, per: Union[str, timedelta] = 'minute'):
        if count <= 0:
            raise ValueError('Speed must be greater than zero.')
        if isinstance(per, str):
            if per.lower() not in _ALIASES:
                raise ValueError(
                    f'Unknown period {per!r}. Use one of: {", ".join(_PERIODS)}.')
            per = _PERIODS[_ALIASES[per.lower()]]
        if per.total_seconds() <= 0:
            raise ValueError('Period must be longer than zero.')
        # exact arithmetic: 15 per minute times 2 weeks is exactly 302400
        self._rate: Fraction = exact(count) / seconds(per)
        self._per_second: float = float(self._rate)

    @property
    def per_second(self) -> float:
        return self._per_second

    @property
    def per_minute(self) -> float:
        return self._per_second * 60

    @property
    def per_hour(self) -> float:
        return self._per_second * 3600

    @property
    def per_day(self) -> float:
        return self._per_second * 86400

    @property
    def per_week(self) -> float:
        return self._per_second * 604800

    def attempts(self, duration: timedelta) -> Fraction:
        """Exact number of passwords that can be tried during ``duration``."""
        return self._rate * seconds(duration)

    def __mul__(self, duration: timedelta) -> float:
        """Number of passwords that can be tried during ``duration``."""
        if not isinstance(duration, timedelta):
            return NotImplemented
        return float(self.attempts(duration))

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Speed):
            return NotImplemented
        return self._rate == other._rate

    __hash__ = None  # type: ignore[assignment]

    def __repr__(self) -> str:
        return f'Speed({self.per_minute:g}, per="minute")'

    @classmethod
    def parse(cls, text: str) -> Speed:
        """Build a speed from a string like ``15/min``, ``100/day`` or ``3/m``.

        >>> Speed.parse('100/day').per_day
        100.0
        """
        count, slash, period = text.replace(' ', '').partition('/')
        try:
            value = float(count)
        except ValueError:
            value = None
        if value is None or not slash or not period:
            raise ValueError(
                f'Cannot read speed {text!r}. Use "<count>/<period>", '
                f'for example "15/min" or "100/day".')
        return cls(value, per=period)
