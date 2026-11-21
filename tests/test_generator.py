import string

import pytest

from pwdgenerator import Duration, Generator, Speed, required_length
from pwdgenerator.alphabets import DIGITS, ENG_LOWER, ENG_UPPER, SYMBOLS


def test_required_length_matches_formula():
    # S* = V*T/P = 10 * 10 / 1e-4 = 1e6, so ten digits give exactly 10^6
    assert required_length(10, 1e-4, Speed(10), Duration(minutes=10)) == 6
    # one more attempt and six digits are not enough
    assert required_length(10, 1e-4, Speed(10.0001), Duration(minutes=10)) == 7


@pytest.mark.parametrize('A, P, V, T', [
    (94, 1e-4, Speed(15), Duration(weeks=2)),
    (62, 1e-7, Speed(100, 'day'), Duration(days=10)),
    (26, 1e-5, Speed(3), Duration(days=10)),
    (2, 1, Speed(1), Duration(minutes=1)),
])
def test_required_length_is_the_smallest(A, P, V, T):
    L = required_length(A, P, V, T)
    lower_bound = V * T / P
    assert A ** L >= lower_bound
    assert L == 1 or A ** (L - 1) < lower_bound


def test_required_length_validation():
    with pytest.raises(ValueError):
        required_length(1, 1e-4, Speed(1), Duration(days=1))
    with pytest.raises(ValueError):
        required_length(10, 0, Speed(1), Duration(days=1))
    with pytest.raises(ValueError):
        required_length(10, 2, Speed(1), Duration(days=1))


def test_generate_by_params():
    generator = Generator(string.ascii_letters + string.digits)
    password = generator.generate_by_params(P=1e-4, V=Speed(15), T=Duration(weeks=2))
    assert password.A == 62
    assert password.L == len(password.password) == 6
    assert set(password.password) <= set(generator.alphabet)
    assert password.lower_bound == pytest.approx(302400 / 1e-4)
    assert password.probability <= 1e-4
    assert password.entropy == pytest.approx(6 * 5.954, rel=1e-3)
    assert str(password) == password.password


def test_min_length():
    generator = Generator(DIGITS, min_length=12)
    password = generator.generate_by_params(P=0.5, V=Speed(1), T=Duration(minutes=1))
    assert password.L == 12


def test_generate():
    generator = Generator('ab')
    password = generator.generate(200)
    assert len(password) == 200
    assert set(password) == {'a', 'b'}


def test_alphabet_is_deduplicated():
    assert Generator('aabbc').A == 3


@pytest.mark.parametrize('alphabet', ['', 'aaaa'])
def test_alphabet_validation(alphabet):
    with pytest.raises(ValueError):
        Generator(alphabet)


def test_generate_by_templates():
    templates = [ENG_UPPER, ENG_UPPER, [4], DIGITS, SYMBOLS, ENG_LOWER]
    copy = [list(t) if not isinstance(t, str) else t for t in templates]
    password = Generator.generate_by_templates(templates)
    assert len(password) == 6
    assert password[0] in ENG_UPPER and password[1] in ENG_UPPER
    assert password[2] == '4'
    assert password[3] in DIGITS and password[4] in SYMBOLS and password[5] in ENG_LOWER
    # the templates are not changed
    assert [list(t) if not isinstance(t, str) else t for t in templates] == copy


def test_empty_template():
    with pytest.raises(ValueError, match='position 2'):
        Generator.generate_by_templates(['a', []])


def test_passwords_are_random():
    generator = Generator()
    assert len({generator.generate(20) for _ in range(50)}) == 50
