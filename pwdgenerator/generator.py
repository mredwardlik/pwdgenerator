from __future__ import annotations

import math
import secrets
from datetime import timedelta
from typing import Any, Iterable, Optional, Sequence

from pwdgenerator.alphabets import DEFAULT
from pwdgenerator.duration import Duration
from pwdgenerator.password import Password
from pwdgenerator.speed import Speed, exact

__all__ = ['Generator', 'required_length']


def required_length(A: int, P: float, V: Speed, T: timedelta) -> int:
    """Smallest password length ``L`` that satisfies Anderson's formula.

    The formula says that ``S = A ** L`` passwords must be at least
    ``S* = V * T / P``. Integers are used for the final check, so the result
    has no rounding errors even when ``S*`` is an exact power of ``A``.

    >>> required_length(A=10, P=1e-4, V=Speed(10, 'minute'), T=Duration(minutes=10))
    6
    """
    if A < 2:
        raise ValueError('The alphabet needs at least two different characters.')
    if not 0 < P <= 1:
        raise ValueError('Probability P must be in the range (0, 1].')
    lower_bound = V.attempts(T) / exact(P)
    if lower_bound <= 1:
        return 1
    length = max(1, math.ceil(math.log(float(lower_bound), A)))
    while A ** length < lower_bound:
        length += 1
    while length > 1 and A ** (length - 1) >= lower_bound:
        length -= 1
    return length


class Generator:
    """Generates passwords with a cryptographically secure random source.

    :param alphabet: characters a password can contain. Repeated characters
        are counted once.
    :param min_length: passwords are never shorter than this.
    """

    def __init__(self, alphabet: Iterable[str] = DEFAULT, min_length: Optional[int] = None):
        chars = ''.join(dict.fromkeys(''.join(alphabet)))
        if len(chars) < 2:
            raise ValueError('The alphabet needs at least two different characters.')
        if min_length is not None and min_length < 1:
            raise ValueError('min_length must be a positive number.')
        self.alphabet: str = chars
        self.min_length: Optional[int] = min_length

    @property
    def A(self) -> int:
        """Size of the alphabet."""
        return len(self.alphabet)

    def generate(self, length: int) -> str:
        """A random password of the given length."""
        if length < 1:
            raise ValueError('Length must be a positive number.')
        return ''.join(secrets.choice(self.alphabet) for _ in range(length))

    # name used in the original lab code
    generate_by_length = generate

    def generate_by_params(self, P: float, V: Speed, T: timedelta) -> Password:
        """A password that an attacker guesses during ``T`` with a probability
        not higher than ``P``, trying ``V`` passwords per unit of time.

        >>> gen = Generator('0123456789')
        >>> pwd = gen.generate_by_params(P=1e-4, V=Speed(10, 'minute'), T=Duration(minutes=10))
        >>> pwd.L
        6
        """
        length = required_length(self.A, P, V, T)
        if self.min_length is not None:
            length = max(length, self.min_length)
        if not isinstance(T, Duration):
            T = Duration(seconds=T.total_seconds())
        return Password(self.generate(length), A=self.A, P=P, V=V, T=T)

    @staticmethod
    def generate_by_templates(templates: Sequence[Iterable[Any]]) -> str:
        """A password built position by position.

        Every item of ``templates`` is the set of characters allowed at that
        position: a string, or any collection of characters and numbers.

        >>> Generator.generate_by_templates(['A', 'b', [7], 'xyz'])[:3]
        'Ab7'
        """
        password = []
        for position, template in enumerate(templates, start=1):
            choices = [str(item) for item in (template if not isinstance(template, str) else list(template))]
            if not choices:
                raise ValueError(f'Template at position {position} is empty.')
            password.append(secrets.choice(choices))
        return ''.join(password)
