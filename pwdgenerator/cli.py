"""Command line interface: ``pwdgenerator --help``."""

from __future__ import annotations

import argparse
import sys
from typing import Callable, Optional, Sequence, TypeVar

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from pwdgenerator import __version__
from pwdgenerator.alphabets import resolve
from pwdgenerator.duration import Duration
from pwdgenerator.generator import Generator
from pwdgenerator.speed import Speed
from pwdgenerator.vigenere import Vigenere

T = TypeVar('T')
DEFAULT_SPEC = 'lower+upper+digits+symbols'


def _typed(parse: Callable[[str], T]) -> Callable[[str], T]:
    """Show the parser's own message when an argument is wrong."""
    def wrapper(value: str) -> T:
        try:
            return parse(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError(str(error)) from None
    wrapper.__name__ = parse.__name__
    return wrapper


def _probability(value: str) -> float:
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f'{value!r} is not a number.') from None
    if not 0 < number <= 1:
        raise ValueError('Probability must be in the range (0, 1], for example 1e-4.')
    return number


def _positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise ValueError('The number must be positive.')
    return number


def _add_alphabet(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-a', '--alphabet', default=DEFAULT_SPEC, metavar='SETS',
        help='character sets joined with "+": lower, upper, digits, symbols, '
             'ru-lower, ru-upper (default: %(default)s)')
    group.add_argument('-c', '--chars', metavar='CHARS', help='use exactly these characters')


def _generator(args: argparse.Namespace) -> Generator:
    alphabet = args.chars if args.chars else resolve(args.alphabet)
    return Generator(alphabet, min_length=getattr(args, 'min_length', None))


def _number(value: float) -> str:
    if value >= 1e6 or value < 1e-3:
        return f'{value:.3e}'
    return f'{value:,.2f}'.rstrip('0').rstrip('.').replace(',', ' ')


def cmd_random(args: argparse.Namespace, console: Console) -> None:
    generator = _generator(args)
    for _ in range(args.count):
        console.print(Text(generator.generate(args.length), style='bold green'), soft_wrap=True)


def cmd_params(args: argparse.Namespace, console: Console) -> None:
    generator = _generator(args)
    password = generator.generate_by_params(P=args.P, V=args.V, T=args.T)

    table = Table.grid(padding=(0, 2))
    table.add_column(style='cyan', justify='right')
    table.add_column()
    table.add_column(style='dim')
    table.add_row('P', str(args.P), 'probability of guessing during T')
    table.add_row('V', f'{_number(args.V.per_minute)} / min', f'{_number(args.V.per_day)} passwords a day')
    table.add_row('T', f'{_number(args.T.total_days)} days', f'{_number(args.T.total_minutes)} minutes')
    table.add_row('S*', _number(password.lower_bound), 'S* = V · T / P')
    table.add_row('A', str(password.A), 'alphabet size')
    table.add_row('L', str(password.L), 'smallest L with A^L ≥ S*' + (' (raised by --min-length)' if generator.min_length and generator.min_length == password.L else ''))
    table.add_row('', '', '')
    table.add_row('entropy', f'{password.entropy:.1f} bits', '')
    table.add_row('real P', f'{password.probability:.3e}', 'V · T / A^L')

    console.print(Panel(
        table,
        title=Text(password.password, style='bold green'),
        title_align='left',
        border_style='magenta',
        expand=False,
    ))


def cmd_vigenere(args: argparse.Namespace, console: Console) -> None:
    cipher = Vigenere(args.chars if args.chars else resolve(args.alphabet))
    action = cipher.encrypt if args.command == 'encrypt' else cipher.decrypt
    text = args.text if args.text is not None else sys.stdin.read().rstrip('\n')
    console.print(Text(action(text, args.key)), soft_wrap=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='pwdgenerator',
        description="Generate passwords by Anderson's formula and encrypt text with the Vigenère cipher.")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    commands = parser.add_subparsers(dest='command', required=True, metavar='COMMAND')

    random_cmd = commands.add_parser('random', help='random passwords of a fixed length')
    random_cmd.add_argument('-l', '--length', type=_typed(_positive), default=16, help='password length (default: %(default)s)')
    random_cmd.add_argument('-n', '--count', type=_typed(_positive), default=1, help='how many passwords (default: %(default)s)')
    _add_alphabet(random_cmd)
    random_cmd.set_defaults(handler=cmd_random)

    params = commands.add_parser(
        'params', help="password length from Anderson's formula",
        description='Find the shortest password that an attacker guesses during T '
                    'with a probability not higher than P, trying V passwords per unit of time.')
    params.add_argument('-P', type=_typed(_probability), required=True, metavar='PROB', help='probability, for example 1e-4')
    params.add_argument('-V', type=_typed(Speed.parse), required=True, metavar='SPEED', help='guessing speed, for example 15/min or 100/day')
    params.add_argument('-T', type=_typed(Duration.parse), required=True, metavar='TIME', help='attack time, for example 2w, 10d or 1d12h')
    params.add_argument('--min-length', type=_typed(_positive), help='never generate a shorter password')
    _add_alphabet(params)
    params.set_defaults(handler=cmd_params)

    for name in ('encrypt', 'decrypt'):
        cmd = commands.add_parser(name, help=f'{name} text with the Vigenère cipher')
        cmd.add_argument('text', nargs='?', help='text to process (read from stdin if missing)')
        cmd.add_argument('-k', '--key', required=True, help='cipher key')
        cmd.add_argument(
            '-a', '--alphabet', default='en', metavar='NAME',
            help='en, ru or ru-no-yo (default: %(default)s)')
        cmd.add_argument('-c', '--chars', metavar='LETTERS', help='custom alphabet')
        cmd.set_defaults(handler=cmd_vigenere)

    return parser


def main(argv: Optional[Sequence[str]] = None, console: Optional[Console] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    console = console or Console()
    try:
        args.handler(args, console)
    except ValueError as error:
        Console(stderr=True).print(Text.assemble(('error: ', 'red'), str(error)))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
