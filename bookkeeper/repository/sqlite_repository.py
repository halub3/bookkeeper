"""
Модуль БД sqlite
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий SQLite
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls
        self._create()

    def _create(self) -> None:
        """ Костыль создания БД в проекте"""
        names = ', '.join(self.fields.keys())
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({names})')
        con.close()

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError('Forbidden to add object with filled PK')
        names = ', '.join(self.fields.keys())
        answers = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({answers})',
                values
            )
            if cur.lastrowid is not None:
                obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name} WHERE ROWID == {pk}')
            row = cur.fetchone()
        con.close()
        if row is None:
            return None
        ret: T = self.cls(pk=pk, **dict(zip(self.fields, row)))
        return ret

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if where is None:
                cur.execute(f'SELECT ROWID, * FROM {self.table_name}')
            else:
                cond = ' AND '.join(f'{field} = ?' for field in where.keys())
                cur.execute(
                    f'SELECT ROWID, * FROM {self.table_name} WHERE {cond}',
                    list(where.values())
                )
            rows = cur.fetchall()
        con.close()
        return [self.cls(pk=row[0], **dict(zip(self.fields, row[1:]))) for row in rows]

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        fields = ', '.join(f'{field}=?' for field in self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'UPDATE {self.table_name} SET {fields} WHERE ROWID = {obj.pk}',
                values
            )
            if cur.rowcount == 0:
                raise ValueError('Cannot find Primary key to Update')
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE ROWID = {pk}')
            if cur.rowcount == 0:
                raise KeyError('Cannot find Primary key to Delete')
        con.close()
