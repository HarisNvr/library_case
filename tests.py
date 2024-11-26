import sys
from io import StringIO
from sqlite3 import connect

import pytest

from constants import DB_PATH
from database import (
    add_book, view_library, find_books, delete_book, change_book_status,
    db_initialization
)
from funcs import validate_book_year, book_parse, get_search_criteria
from main import main


@pytest.fixture
def capsys_mock():
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    yield sys.stdout
    sys.stdout = old_stdout


# УДАЛИТЕ ФАЙЛ БАЗЫ 'Library.db' ЕСЛИ ОН У ВАС СОЗДАН, ИНАЧЕ ТЕСТЫ БУДУТ ПАДАТЬ


def test_db_initialization():
    db_initialization(DB_PATH)

    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name FROM sqlite_master '
            'WHERE type="table" AND name="Books"'
        )
        assert cursor.fetchone() is not None


def test_add_book():
    message = add_book('Преступление и наказание', 'Фёдор Достоевский', 1866)
    assert (
            '"Книга \"Преступление и наказание\" "'
            'автора Фёдор Достоевский добавлена' in message
    )


def test_view_library():
    add_book('Анна Каренина', 'Лев Толстой', 1877)
    books = view_library()
    assert len(books) == 2
    assert books[0][1] == 'Преступление и наказание'
    assert books[1][1] == 'Анна Каренина'


def test_find_book():
    result = find_books(book_id=1)
    assert result[0][1] == 'Преступление и наказание'

    result = find_books(title='Преступление и наказание')
    assert result[0][2] == 'Фёдор Достоевский'

    result = find_books(author='Фёдор Достоевский')
    assert result[0][3] == 1866

    result = find_books(year=1866)
    assert result[0][0] == 1


def test_delete_book():
    add_book('Преступление и наказание', 'Фёдор Достоевский', 1866)
    message = delete_book(3)
    assert 'Книга с ID 3 удалена успешно' in message
    assert len(view_library()) == 2


def test_change_book_status():
    change_book_status(1, 'В наличии')

    result = find_books(book_id=1)
    assert result[0][4] == 'Выдана'


def test_validate_book_year():
    assert validate_book_year('2000') == 2000
    assert validate_book_year('3000') is False
    assert validate_book_year('abcd') is False


def test_book_parse(capsys):
    books = [
        (
            1, 'Преступление и наказание', 'Фёдор Достоевский',
            1866, 'Выдана'
        ),
        (
            2, 'Анна Каренина', 'Лев Толстой', 1877, 'В наличии'
        ),
    ]

    book_parse(books, header='Список книг:')
    captured = capsys.readouterr().out

    assert 'Список книг:' in captured
    assert 'Преступление и наказание' in captured
    assert 'Анна Каренина' in captured


def test_main_menu(capsys, monkeypatch):
    inputs = iter(['q'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr().out

    assert '1) Добавить книгу' in captured
    assert '2) Удалить книгу' in captured
    assert '3) Поиск книг' in captured
    assert '4) Отобразить все книги' in captured
    assert 'q - Выход из программы' in captured


def test_get_search_criteria(capsys_mock, monkeypatch):
    inputs = iter(['1', 'Преступление и наказание', 'q'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    criteria = get_search_criteria()
    assert criteria == {'title': 'Преступление и наказание'}


if __name__ == '__main__':
    pytest.main()
