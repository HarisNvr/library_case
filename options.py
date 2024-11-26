from funcs import (
    cls, check_cancel, validate_book_year, book_parse, confirm_action,
    get_search_criteria
)
from database import (
    add_book, find_books, delete_book, view_library, change_book_status
)


def add_book_option():
    """
    Обрабатывает ввод пользователя для добавления новой книги.
    """

    cls()
    print(
        'Вы выбрали опцию "Добавить книгу"'
        '\n'
        '\nЕсли хотите отменить добавление книги и вернуться в главное '
        'меню, то на любом из этапов введите "q"'
        '\n'
    )

    # Как вариант: добавить обработку по длине названия или автора.
    book_name = input('Пожалуйста укажите название книги: ')
    if check_cancel(book_name):
        return

    book_author = input('Пожалуйста укажите автора книги: ')
    if check_cancel(book_author):
        return

    book_year = input('Пожалуйста укажите год издания книги: ')
    if check_cancel(book_year):
        return
    validated_book_year = validate_book_year(book_year)
    if validated_book_year:
        print(add_book(book_name, book_author, validated_book_year))

    print('')


def delete_book_option():
    """
    Обрабатывает ввод пользователя для удаления книги.
    """

    cls()
    print(
        'Вы выбрали опцию "Удалить книгу"'
        '\n'
        '\nЕсли хотите отменить удаление книги и вернуться в главное '
        'меню, то введите "q"'
        '\n'
    )

    user_input_delete = input('Введите ID книги, которую хотите удалить: ')
    if check_cancel(user_input_delete):
        return

    try:
        book_id = int(user_input_delete)
        result = find_books(book_id=book_id)

        if isinstance(result, str):
            print(result)
        else:
            print('\nВы хотите удалить следующую книгу: ')
            book_parse(result)
            if confirm_action('Вы уверены, что хотите удалить эту книгу?'):
                print(delete_book(book_id))
            else:
                print('Операция отменена.')
    except ValueError:
        print(
            'ID книги должен быть целым числом!'
            '\nВозврат в главное меню.'
        )


def find_books_option() -> None:
    """
    Обрабатывает ввод пользователя для поиска книги.
    """

    cls()
    print('Вы выбрали опцию "Поиск книг"\n')

    criteria = get_search_criteria()

    if not criteria:
        return

    key, value = list(criteria.items())[0]
    result = find_books(**{key: value})

    cls()

    if isinstance(result, str):
        print(result)
    else:
        book_parse(result, header='Результаты поиска:')


def view_library_option() -> None:
    """
    Отображает все книги из библиотеки.
    """
    books = view_library()
    book_parse(books, header='Список всех книг:')


def change_book_status_option():
    """
    Обрабатывает ввод пользователя для изменения статуса книги.
    """

    cls()
    print(
        'Вы выбрали опцию "Изменение статуса книги"'
        '\n'
        '\nЕсли хотите отменить изменение статуса книги и вернуться в главное '
        'меню, то введите "q"'
        '\n'
    )

    user_input_change = input(
        'Введите ID книги, которой хотите изменить статус: '
    )
    if check_cancel(user_input_change):
        return

    try:
        book_id = int(user_input_change)
        result = find_books(book_id=book_id)
        book_status = result[0][4]

        if isinstance(result, str):
            print(result)
        else:
            print('\nВы хотите изменить статус у следующей книги: ')
            book_parse(result)
            if confirm_action(
                    'Вы уверены, что хотите изменить статус этой книги?'
            ):
                print(
                    change_book_status(
                        book_id=book_id,
                        current_status=book_status
                    )
                )
            else:
                print('Операция отменена.')
    except ValueError:
        print(
            'ID книги должен быть целым числом!'
            '\nВозврат в главное меню.'
        )
