# Библиотечная система управления

Это консольное приложение для управления библиотекой книг. Оно позволяет добавлять, удалять, искать и отображать книги в библиотеке, а также изменять их статус.

## Описание

Приложение использует SQLite для хранения данных о книгах и предоставляет пользователю интерфейс для выполнения операций через командную строку. Использование ООП здесь нецелесообразно, т.к. для БД я выбрал SQLite, а для работы с ней через ООП необходимы как минимум SQLAlchemy и Alembic, которые по условию запрещено использовать.

### Функции:
- **Добавление книги**: Добавляет новую книгу с заданным названием, автором и годом издания.
- **Удаление книги**: Удаляет книгу по её ID.
- **Поиск книги**: Позволяет искать книги по названию, автору или году издания.
- **Отображение всех книг**: Показывает список всех книг в библиотеке.
- **Изменение статуса книги**: Позволяет изменить статус книги на "В наличии" или "Выдана".

## Структура проекта

- **`main.py`** — основной файл приложения, который запускает интерфейс командной строки.
- **`database.py`** — модуль для работы с базой данных (SQLite), содержащий функции для добавления, удаления, поиска и обновления книг.
- **`options.py`** — модуль отвечающий за ввод/вывод данных в меню.
- **`funcs.py`** — вспомогательные функции.
- **`constants.py`** — файл с константами.
- **`tests.py`** — файл с тестами для проверки корректности работы приложения.

## Установка

1. Клонируйте репозиторий на свою машину:

    ```bash
    git clone https://github.com/HarisNvr/library_case.git
    cd library_case
    ```

2. Cоздать и активировать виртуальное окружение:
    * Windows
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/Scripts/activate
    ```

    * Linux/macOS
    ```bash
    python3 -m venv venv
    ```
    ```bash
    source venv/bin/activate
    ```

3. Установить pytest:

    ```bash
    pip install pytest
    ```

## Использование

1. Запустите приложение:

    * Windows
    ```bash
    python main.py
    ```
   
    * Linux/macOS
    ```bash
    python3 main.py
    ```

2. В меню выберите одну из опций:
   - `1`: Добавить книгу
   - `2`: Удалить книгу
   - `3`: Поиск книг
   - `4`: Показать все книги
   - `5`: Изменить статус книги
   - `q`: Выход из программы

Введите номер опции в консоль и нажмите "enter" в зависимости от выбранного пункта меню у вас отобразится новое меню, в котором необходимо будет сделать новый выбор.

Если вы хотите вернуться в главное меню или закончить выполнение программы, когда находитесь в главном меню - введите букву "q" вместо цифр.

## Тестирование

* Обязательно удалите файл с БД, если ранее запускали программу. Тесты сами создадут чистую БД и будут тестировать на ней.

```bash
pytest tests.py
```
