import io

import pytest
from rich.console import Console

from pwdgenerator.cli import main


def run(*argv):
    output = io.StringIO()
    code = main(list(argv), console=Console(file=output, width=120, color_system=None))
    return code, output.getvalue()


def test_random():
    code, out = run('random', '-l', '12', '-n', '3', '-a', 'digits')
    lines = out.split()
    assert code == 0 and len(lines) == 3
    assert all(len(line) == 12 and line.isdigit() for line in lines)


def test_random_custom_chars():
    code, out = run('random', '-l', '30', '-c', 'xy')
    assert code == 0 and set(out.strip()) <= {'x', 'y'}


def test_params():
    code, out = run('params', '-P', '1e-4', '-V', '15/min', '-T', '2w', '-a', 'lower+upper+digits')
    assert code == 0
    assert 'S*' in out and '62' in out
    assert 'entropy' in out


def test_params_bad_speed(capsys):
    with pytest.raises(SystemExit):
        run('params', '-P', '1e-4', '-V', 'fast', '-T', '2w')
    assert 'Cannot read speed' in capsys.readouterr().err


def test_encrypt_decrypt():
    assert run('encrypt', 'Attack at dawn!', '-k', 'lemon')[1].strip() == 'Lxfopv ef rnhr!'
    assert run('decrypt', 'Lxfopv ef rnhr!', '-k', 'lemon')[1].strip() == 'Attack at dawn!'


def test_encrypt_bad_key():
    code, _ = run('encrypt', 'hello', '-k', '123')
    assert code == 2
