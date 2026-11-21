"""Лабораторная работа 1: длина пароля по формуле Андерсона.

Для каждого из 30 вариантов задания (P, V, T) генерирует пароль минимальной
длины, которую злоумышленник подберёт за время T с вероятностью не выше P.
"""

from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich.text import Text

from pwdgenerator import Duration, Generator, Speed
from pwdgenerator.alphabets import DEFAULT

console = Console()

# (P, V, T) для вариантов 1–30
VARIANTS = [
    (1e-4, Speed(15, 'minute'), Duration(weeks=2)),
    (1e-5, Speed(3, 'minute'), Duration(days=10)),
    (1e-6, Speed(10, 'minute'), Duration(days=5)),
    (1e-7, Speed(11, 'minute'), Duration(days=6)),
    (1e-4, Speed(100, 'day'), Duration(days=12)),
    (1e-5, Speed(10, 'day'), Duration(days=30)),
    (1e-6, Speed(20, 'minute'), Duration(weeks=3)),
    (1e-7, Speed(15, 'minute'), Duration(days=20)),
    (1e-4, Speed(3, 'minute'), Duration(days=15)),
    (1e-5, Speed(10, 'minute'), Duration(weeks=1)),
    (1e-6, Speed(11, 'minute'), Duration(weeks=2)),
    (1e-7, Speed(100, 'day'), Duration(days=10)),
    (1e-4, Speed(10, 'day'), Duration(days=5)),
    (1e-5, Speed(20, 'minute'), Duration(days=6)),
    (1e-6, Speed(15, 'minute'), Duration(days=12)),
    (1e-7, Speed(3, 'minute'), Duration(days=30)),
    (1e-4, Speed(10, 'minute'), Duration(weeks=3)),
    (1e-5, Speed(11, 'minute'), Duration(days=20)),
    (1e-6, Speed(100, 'day'), Duration(days=15)),
    (1e-7, Speed(10, 'day'), Duration(weeks=1)),
    (1e-4, Speed(20, 'minute'), Duration(weeks=2)),
    (1e-5, Speed(15, 'minute'), Duration(days=10)),
    (1e-6, Speed(3, 'minute'), Duration(days=5)),
    (1e-7, Speed(10, 'minute'), Duration(days=6)),
    (1e-4, Speed(11, 'minute'), Duration(days=12)),
    (1e-5, Speed(100, 'day'), Duration(days=30)),
    (1e-6, Speed(10, 'day'), Duration(weeks=3)),
    (1e-7, Speed(20, 'minute'), Duration(days=20)),
    (1e-4, Speed(15, 'minute'), Duration(days=15)),
    (1e-5, Speed(3, 'minute'), Duration(weeks=1)),
]


def main() -> None:
    chars = console.input(
        'Введите набор символов для генерации пароля или нажмите [cyan]Enter[/cyan]: ')
    chars = chars or DEFAULT
    console.print(f'Набор символов для генерации: [magenta]{escape(chars)}[/magenta]', highlight=False)

    generator = Generator(chars, min_length=6)

    table = Table(header_style='bold magenta', show_lines=True)
    for column in ('Вариант', 'Пароль', 'A', 'L', 'P', 'V (паролей/день)', 'T (дней)'):
        table.add_column(column)

    for number, (P, V, T) in enumerate(VARIANTS, start=1):
        password = generator.generate_by_params(P=P, V=V, T=T)
        table.add_row(
            str(number),
            Text(password.password),  # not rich markup
            str(password.A),
            str(password.L),
            f'{P:g}',
            f'{V.per_day:g}',
            f'{T.total_days:g}',
        )

    console.print(table)


if __name__ == '__main__':
    main()
