import pytest
import sqlite3
from dataclasses import dataclass

from bookkeeper.repository.sqlite_repository import SQLiteRepository

DB_FILE = "databases/test_sql.db"
TEST_FIELD_INT = 11
TEST_FIELD_STR = "test field value"

@pytest.fixture
def create_bd():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS custom")
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS custom(field_int int, field_str str)")
    con.close()


@pytest.fixture
def custom_class():
    @dataclass
    class Custom():
        field_int: int = TEST_FIELD_INT
        field_str: str = TEST_FIELD_STR
        pk: int = 0
    return Custom


@pytest.fixture
def repo(custom_class, create_bd):
    return SQLiteRepository(db_file=DB_FILE, cls=custom_class)

def test_crud(repo, custom_class):
    #ADD
    obj_add = custom_class()
    pk = repo.add(obj_add)
    assert obj_add.pk == pk

    #GET
    obj_get = repo.get(pk)
    assert obj_get is not None
    assert obj_get.pk == pk
    assert obj_get.field_int == obj_add.field_int
    assert obj_get.field_str == obj_add.field_str

    #UPDATE
    obj_upd = custom_class(100, "new str val", pk)
    repo.update(obj_upd)
    obj_get_upd = repo.get(pk)
    assert obj_get_upd.pk == obj_upd.pk
    assert obj_get_upd.field_str == obj_upd.field_str
    assert obj_get_upd.field_int == obj_upd.field_int

    #DELETE
    repo.delete(pk)
    assert repo.get(pk) is None

def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects

def test_get_all_with_condition(repo, custom_class):
    objs_add_all = []
    str_to_find = "founded str"
    obj_new = custom_class(field_int=150, field_str=str_to_find + 'salt')
    repo.add(obj_new)
    for idx in range(4):
        obj_new = custom_class(field_int=idx ** 2, field_str=str_to_find)
        repo.add(obj_new)
        objs_add_all.append(obj_new)
    where_succ = {'field_str': str_to_find}
    where_fail = {'field_int': -1}
    objs_get_all = repo.get_all(where_succ)
    obj_none = repo.get_all(where_fail)
    assert obj_none == []
    assert objs_get_all == objs_add_all





