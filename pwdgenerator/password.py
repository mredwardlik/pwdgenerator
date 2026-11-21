from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from pwdgenerator.duration import Duration
from pwdgenerator.speed import Speed

__all__ = ['Password']


@dataclass(frozen=True)
class Password:
    """A generated password and the parameters it was generated with.

    The single-letter names follow the notation of Anderson's formula:

    * ``A``: size of the alphabet
    * ``L``: length of the password
    * ``P``: probability that the password is guessed during ``T``
    * ``V``: guessing speed
    * ``T``: time the attacker has
    """

    password: str = field(repr=False)
    A: int
    P: Optional[float] = None
    V: Optional[Speed] = None
    T: Optional[Duration] = None

    @property
    def L(self) -> int:
        return len(self.password)

    @property
    def S(self) -> int:
        """Number of possible passwords: ``A ** L``."""
        return self.A ** self.L

    @property
    def lower_bound(self) -> Optional[float]:
        """``S* = V * T / P``: the smallest ``S`` that satisfies the formula."""
        if self.P is None or self.V is None or self.T is None:
            return None
        return self.V * self.T / self.P

    @property
    def probability(self) -> Optional[float]:
        """Real probability of guessing this password during ``T``."""
        if self.V is None or self.T is None:
            return None
        return min(1.0, self.V * self.T / self.S)

    @property
    def entropy(self) -> float:
        """Password strength in bits."""
        return self.L * math.log2(self.A) if self.A > 1 else 0.0

    def __str__(self) -> str:
        return self.password

    def __len__(self) -> int:
        return self.L
