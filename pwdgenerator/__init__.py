"""Password generation by Anderson's formula and by templates, plus the
Vigenère cipher."""

from pwdgenerator.duration import Duration
from pwdgenerator.generator import Generator, required_length
from pwdgenerator.password import Password
from pwdgenerator.speed import Speed
from pwdgenerator.vigenere import Vigenere

__version__ = '1.0.0'
__all__ = ['Duration', 'Generator', 'Password', 'Speed', 'Vigenere', 'required_length']
