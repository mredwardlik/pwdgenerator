import pytest

from pwdgenerator import Vigenere
from pwdgenerator.alphabets import ENG_LOWER, RUS_LOWER


def test_classic_example():
    cipher = Vigenere(ENG_LOWER)
    assert cipher.encrypt('ATTACKATDAWN', 'LEMON') == 'LXFOPVEFRNHR'
    assert cipher.decrypt('LXFOPVEFRNHR', 'LEMON') == 'ATTACKATDAWN'


def test_keeps_case_and_other_characters():
    cipher = Vigenere(ENG_LOWER)
    assert cipher.encrypt('Attack at dawn!', 'lemon') == 'Lxfopv ef rnhr!'


def test_russian():
    cipher = Vigenere(RUS_LOWER)
    text = 'Привет, мир! Шифр Виженера.'
    encrypted = cipher.encrypt(text, 'ключ')
    assert encrypted != text
    assert cipher.decrypt(encrypted, 'КЛЮЧ') == text


def test_key_with_spaces_and_case():
    cipher = Vigenere(ENG_LOWER)
    assert cipher.encrypt('hello', 'Ab C') == cipher.encrypt('hello', 'abc')


@pytest.mark.parametrize('key', ['', '   ', 'key1', 'ключ'])
def test_wrong_key(key):
    with pytest.raises(ValueError):
        Vigenere(ENG_LOWER).encrypt('hello', key)


def test_wrong_alphabet():
    with pytest.raises(ValueError):
        Vigenere('abca')
    with pytest.raises(ValueError):
        Vigenere('a')
