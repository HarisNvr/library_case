from datetime import datetime
from os import system, name
from typing import Union

CURRENT_YEAR = datetime.now().year


def cls():
    """
    Очищает консоль.
    """

    system('cls' if name == 'nt' else 'clear')


def check_cancel(input_value: str) -> bool:
    """
    Проверяет, ввёл ли пользователь символ 'q' для отмены.

    :param input_value: Строка, введённая пользователем.
    :return: True, если ввод 'q', иначе False.
    """
    if input_value.lower() == 'q':
        print('\nОперация отменена, возврат в главное меню.')
        return True

    return False


def validate_book_year(year_to_validate: str) -> Union[int, bool]:
    """
    Проверяет корректность года издания книги.

    :param year_to_validate: Год книги в виде строки.
    :return: Год как int, если он валиден, иначе False.
    """

    try:
        book_year = int(year_to_validate)
        if book_year > CURRENT_YEAR:
            print(
                'Год издания книги не может быть больше, чем текущий!'
                '\nВозврат в главное меню.'
            )
            return False
        else:
            return book_year
    except ValueError:
        print(
            'Введён некорректный год издания книги! '
            '\nВозврат в главное меню.'
        )
        return False


def book_parse(db_response: list[tuple], header: str = '') -> None:
    """
    Парсит и выводит список книг в читаемом формате.

    :param db_response: Список кортежей, каждый из которых представляет книгу.
    :param header: Заголовок для вывода.
    """
    if header:
        print(header)

    for book in db_response:
        print(
            f'ID:{book[0]} "{book[1]}" автора {book[2]}, '
            f'{book[3]} года издания. Статус: {book[4]}'
        )


def confirm_action(prompt: str) -> bool:
    """
    Запрашивает подтверждение действия у пользователя.

    :param prompt: Сообщение для запроса подтверждения.
    :return: True, если пользователь ввёл 'y', иначе False.
    """
    confirmation = input(f'\n{prompt} (y/n): ').lower()
    return confirmation == 'y'


def get_search_criteria() -> dict:
    """
    Запрашивает у пользователя критерий для поиска книги.

    :return: Словарь с ключом (название поля) и значением для поиска.
    """
    print(
        'Выберите критерий для поиска:\n'
        '1) Название\n'
        '2) Автор\n'
        '3) Год издания\n'
        'q - Отмена\n'
    )

    choice = input('Введите номер критерия: ')
    if check_cancel(choice):
        return {}

    if choice == '1':
        value = input('Введите название книги: ')
        return {'title': value}
    elif choice == '2':
        value = input('Введите автора книги: ')
        return {'author': value}
    elif choice == '3':
        value = input('Введите год издания книги: ')
        year = validate_book_year(value)
        if year:
            return {'year': year}

    print('Некорректный выбор.')
    return {}
