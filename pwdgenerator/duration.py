from __future__ import annotations

import re
from datetime import timedelta

__all__ = ['Duration']

_UNITS = {
    's': 'seconds', 'sec': 'seconds', 'second': 'seconds', 'seconds': 'seconds',
    'm': 'minutes', 'min': 'minutes', 'minute': 'minutes', 'minutes': 'minutes',
    'h': 'hours', 'hour': 'hours', 'hours': 'hours',
    'd': 'days', 'day': 'days', 'days': 'days',
    'w': 'weeks', 'week': 'weeks', 'weeks': 'weeks',
}
_PART = re.compile(r'(\d+(?:\.\d+)?)\s*([a-z]+)')


class Duration(timedelta):
    """A period of time, the ``T`` in Anderson's formula.

    It is a regular :class:`datetime.timedelta`, so it accepts the same
    arguments (``weeks``, ``days``, ``hours``, ``minutes`` ...) and adds a few
    helpers to read the length in the units used by the formula.

    >>> Duration(weeks=2).total_days
    14.0
    """

    @property
    def total_minutes(self) -> float:
        return self.total_seconds() / 60

    @property
    def total_hours(self) -> float:
        return self.total_seconds() / 3600

    @property
    def total_days(self) -> float:
        return self.total_seconds() / 86400

    @property
    def total_weeks(self) -> float:
        return self.total_seconds() / 604800

    @classmethod
    def parse(cls, text: str) -> Duration:
        """Build a duration from a short string like ``2w``, ``10d`` or ``1d12h``.

        >>> Duration.parse('1w 3d').total_days
        10.0
        """
        source = text.strip().lower()
        parts = _PART.findall(source)
        if not parts or _PART.sub('', source).strip():
            raise ValueError(
                f'Cannot read duration {text!r}. Use a number with a unit, '
                f'for example "30m", "12h", "10d" or "2w".')
        kwargs: dict[str, float] = {}
        for value, unit in parts:
            if unit not in _UNITS:
                raise ValueError(f'Unknown time unit {unit!r} in {text!r}.')
            name = _UNITS[unit]
            kwargs[name] = kwargs.get(name, 0) + float(value)
        duration = cls(**kwargs)
        if duration.total_seconds() <= 0:
            raise ValueError('Duration must be longer than zero.')
        return duration

    def __repr__(self) -> str:
        return f'Duration(days={self.total_days:g})'
