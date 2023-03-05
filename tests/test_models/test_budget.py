from datetime import datetime

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    e = Budget(period=4, category=1, amount=1000, pk=1)
    assert e.period == 4
    assert e.category == 1
    assert e.amount == 1000


def test_create_brief():
    e = Budget(4, 1, 1000)
    assert e.period == 4
    assert e.category == 1
    assert e.amount == 1000


def test_can_add_to_repo(repo):
    e = Budget(4, 1, 1000)
    pk = repo.add(e)
    assert e.pk == pk
