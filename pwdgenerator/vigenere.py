from __future__ import annotations

__all__ = ['Vigenere']


class Vigenere:
    """The Vigenère cipher over any alphabet.

    * the case of every letter is kept;
    * characters that are not in the alphabet (spaces, digits, punctuation)
      are copied as they are and don't use a key letter.

    >>> Vigenere('abcdefghijklmnopqrstuvwxyz').encrypt('Attack at dawn!', 'lemon')
    'Lxfopv ef rnhr!'
    """

    def __init__(self, alphabet: str):
        letters = alphabet.lower()
        if len(set(letters)) != len(letters):
            raise ValueError('The alphabet contains repeated letters.')
        if len(letters) < 2:
            raise ValueError('The alphabet needs at least two letters.')
        self.alphabet: str = letters
        self._index = {char: i for i, char in enumerate(letters)}

    def encrypt(self, text: str, key: str) -> str:
        return self._shift(text, key, 1)

    def decrypt(self, text: str, key: str) -> str:
        return self._shift(text, key, -1)

    def _key_shifts(self, key: str) -> list[int]:
        shifts = [self._index.get(char) for char in key.lower() if not char.isspace()]
        if not shifts:
            raise ValueError('The key must not be empty.')
        if None in shifts:
            wrong = sorted({char for char in key.lower() if not char.isspace() and char not in self._index})
            raise ValueError(f'The key has letters that are not in the alphabet: {"".join(wrong)}')
        return shifts  # type: ignore[return-value]

    def _shift(self, text: str, key: str, direction: int) -> str:
        shifts, size = self._key_shifts(key), len(self.alphabet)
        result, k = [], 0
        for char in text:
            index = self._index.get(char.lower())
            if index is None:
                result.append(char)
                continue
            new = self.alphabet[(index + direction * shifts[k % len(shifts)]) % size]
            result.append(new.upper() if char.isupper() else new)
            k += 1
        return ''.join(result)
