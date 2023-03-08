import sys
from PySide6.QtWidgets import QApplication

from PySide6 import QtWidgets
from bookkeeper.view.main_view import MainWindow
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.presenter.bookkeeper import Bookkeeper
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category

DB_NAME = 'databases/main.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = MainWindow()
    # model = None  # TODO: здесь должна быть модель

    cat_repo = SQLiteRepository[Category](DB_NAME, Category)
    exp_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    bud_repo = SQLiteRepository[Budget](DB_NAME, Budget)

    window = Bookkeeper(view, cat_repo, exp_repo, bud_repo)  # TODO: передать три репозитория
    window.show()
    app.exec_()