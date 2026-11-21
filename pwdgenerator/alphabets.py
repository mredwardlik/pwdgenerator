"""Ready-made character sets for passwords and the Vigenère cipher."""

from string import ascii_lowercase, ascii_uppercase, digits, punctuation

__all__ = [
    'ENG_LOWER', 'ENG_UPPER', 'RUS_LOWER', 'RUS_UPPER', 'RUS_LOWER_NO_YO',
    'DIGITS', 'SYMBOLS', 'PUNCTUATION', 'DEFAULT', 'PRESETS', 'resolve',
]

ENG_LOWER = ascii_lowercase
ENG_UPPER = ascii_uppercase
RUS_LOWER = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
RUS_UPPER = RUS_LOWER.upper()
RUS_LOWER_NO_YO = RUS_LOWER.replace('ё', '')
DIGITS = digits
PUNCTUATION = punctuation
# the ten special characters used in the lab variants
SYMBOLS = '!"#$%&\'()*'

DEFAULT = ENG_LOWER + ENG_UPPER + DIGITS + PUNCTUATION

PRESETS = {
    'lower': ENG_LOWER,
    'upper': ENG_UPPER,
    'digits': DIGITS,
    'symbols': PUNCTUATION,
    'ru-lower': RUS_LOWER,
    'ru-upper': RUS_UPPER,
    'en': ENG_LOWER,
    'ru': RUS_LOWER,
    'ru-no-yo': RUS_LOWER_NO_YO,
}


def resolve(spec: str) -> str:
    """Turn ``"lower+upper+digits"`` into the joined character set."""
    chars = []
    for name in spec.split('+'):
        name = name.strip().lower()
        if name not in PRESETS:
            raise ValueError(
                f'Unknown alphabet {name!r}. Available: {", ".join(PRESETS)}.')
        chars.append(PRESETS[name])
    return ''.join(dict.fromkeys(''.join(chars)))
