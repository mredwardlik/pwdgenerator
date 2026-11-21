"""Лабораторная работа 3: шифр Виженера.

Выберите алфавит, затем вводите текст и ключ. Для выхода нажмите Ctrl+C.
"""

from rich.console import Console
from rich.markup import escape

from pwdgenerator import Vigenere
from pwdgenerator.alphabets import ENG_LOWER, RUS_LOWER, RUS_LOWER_NO_YO

console = Console()

ALPHABETS = {
    'Русский': RUS_LOWER,
    'Русский (без ё)': RUS_LOWER_NO_YO,
    'Английский': ENG_LOWER,
    'Свой собственный': None,
}


def choose_alphabet() -> Vigenere:
    names = list(ALPHABETS)
    console.print('Выберите алфавит:')
    for number, name in enumerate(names, start=1):
        console.print(f'  {number}. {name}')
    while True:
        answer = console.input('> ').strip()
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            name = names[int(answer) - 1]
            break
        console.print(f'[red]Введите число от 1 до {len(names)}.[/red]')
    console.print(f'Выбран алфавит: [magenta]{name.lower()}[/magenta]')

    alphabet = ALPHABETS[name]
    while alphabet is None:
        try:
            return Vigenere(console.input('Введите алфавит: ').strip())
        except ValueError as error:
            console.print(f'[red]{escape(str(error))}[/red]')
    return Vigenere(alphabet)


def main() -> None:
    vigenere = choose_alphabet()
    while True:
        console.print()
        text = console.input('Введите текст: ')
        key = console.input('Введите ключ: ')
        try:
            encrypted = vigenere.encrypt(text, key)
            decrypted = vigenere.decrypt(text, key)
        except ValueError as error:
            console.print(f'[red]{escape(str(error))}[/red]')
            continue
        console.print(f'Зашифрованное значение: [magenta]{escape(encrypted)}[/magenta]', highlight=False)
        console.print(f'Расшифрованное значение: [magenta]{escape(decrypted)}[/magenta]', highlight=False)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        console.print()
