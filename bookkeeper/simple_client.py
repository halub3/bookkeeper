"""
Простой тестовый скрипт для терминала
"""

from typing import Any
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
# from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
# from bookkeeper.utils import read_tree

DB_FILE = 'databases/main.db'

cat_repo = SQLiteRepository[Category](DB_FILE, Category)
exp_repo = SQLiteRepository[Expense](DB_FILE, Expense)
bud_repo = SQLiteRepository[Expense](DB_FILE, Budget)

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

# Category.create_from_tree(read_tree(cats), cat_repo)

commands: dict[str, Any] = {
    'категории': cat_repo,
    'расходы': exp_repo,
    'бюджет': bud_repo
}

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd in commands:
        repo = commands[cmd]
        print(*repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
