from sqlite3 import connect
from typing import Union

from constants import DB_PATH


def db_initialization(path: str):
    """
    Инициализирует базу данных, создавая таблицу Books, если она не существует.
    """

    with connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        status TEXT NOT NULL
        )
        ''')


def add_book(title: str, author: str, year: int) -> str:
    """
    Добавляет новую книгу в базу данных.

    :param title: Название книги.
    :param author: Автор книги.
    :param year: Год издания книги.
    :return: Сообщение об успешном добавлении книги.
    """

    sql_prompt = (
        'INSERT INTO Books (title, author, year, status) '
        'VALUES (?, ?, ?, "В наличии")'
    )
    sql_values = (title, author, year)

    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_prompt, sql_values)
        conn.commit()

    return f'\nКнига "{title}" автора {author} добавлена в библиотеку!\n'


def view_library() -> list[tuple]:
    """
    Возвращает список всех книг в библиотеке.

    :return: Список кортежей, где каждый кортеж — книга.
    """

    sql_prompt = 'SELECT * FROM Books'

    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_prompt)
        result = cursor.fetchall()

    return result


def find_books(
        book_id: int = None,
        title: str = None,
        author: str = None,
        year: int = None
) -> Union[list[tuple], str]:
    """
    Ищет книги в базе данных по одному из переданных параметров.

    :param book_id: ID книги.
    :param title: Название книги.
    :param author: Автор книги.
    :param year: Год издания книги.
    :return: Список найденных книг (в виде кортежей) или сообщение, если книги
             не найдены.
    """

    if book_id:
        search_prompt = 'id'
        search_param = book_id
        param_name = 'ID'
    elif title:
        search_prompt = 'title'
        search_param = title
        param_name = 'названием'
    elif author:
        search_prompt = 'author'
        search_param = author
        param_name = 'автором'
    elif year:
        search_prompt = 'year'
        search_param = year
        param_name = 'годом публикации'
    else:
        return 'Не передано ни одного параметра для поиска книг'

    sql_prompt = f'SELECT * FROM Books WHERE {search_prompt} = ?'
    sql_values = (search_param,)

    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_prompt, sql_values)
        result = cursor.fetchall()

    if not result:
        return (
            f'Книг с таким {param_name} не найдено'
        )
    else:
        return result


def delete_book(book_id: int) -> str:
    """
    Удаляет книгу из базы данных по ID.

    :param book_id: ID книги для удаления.
    :return: Сообщение об успешном удалении книги или ошибка.
    """

    sql_prompt = 'DELETE FROM Books WHERE id = ?'
    sql_values = (book_id,)

    search_result = find_books(book_id=book_id)

    if isinstance(search_result, str):
        return search_result
    else:
        with connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_prompt, sql_values)
            conn.commit()
        return f'Книга с ID {book_id} удалена успешно'


def change_book_status(book_id: int, current_status: str) -> str:
    """
    Изменяет статус книги на "В наличии" или "Выдана".

    :param book_id: ID книги.
    :param current_status: Текущий статус книги.
    :return: Сообщение об успешном изменении статуса.
    """

    sql_prompt = 'UPDATE Books SET status = ? WHERE id = ?'

    if current_status == 'В наличии':
        new_status = 'Выдана'
    else:
        new_status = 'В наличии'

    search_result = find_books(book_id=book_id)

    if isinstance(search_result, str):
        return search_result
    else:
        sql_values = (new_status, book_id)
        with connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_prompt, sql_values)
            conn.commit()
        return f'Книга "{search_result[0][1]}" успешно помечена "{new_status}"'
