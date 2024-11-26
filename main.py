from constants import DB_PATH
from options import (
    add_book_option, delete_book_option, find_books_option,
    view_library_option, change_book_status_option
)
from funcs import cls
from database import db_initialization


def main() -> None:
    """
    Точка входа в приложение. Запускает главное меню.
    """

    db_initialization(DB_PATH)
    running = True

    cls()

    while running:
        print(
            '1) Добавить книгу\n'
            '2) Удалить книгу\n'
            '3) Поиск книг\n'
            '4) Отобразить все книги\n'
            '5) Изменение статуса книги\n\n'
            'q - Выход из программы\n'
        )

        user_input = input('Выберите вариант из списка: ')
        print('----------------------------------------')

        if user_input == '1':
            add_book_option()
        elif user_input == '2':
            delete_book_option()
        elif user_input == '3':
            find_books_option()
        elif user_input == '4':
            view_library_option()
        elif user_input == '5':
            change_book_status_option()
        elif user_input == 'q':
            running = False
        else:
            print('Выбран неправильный пункт меню. Повторите выбор.\n')

        print('----------------------------------------')


if __name__ == '__main__':
    main()
