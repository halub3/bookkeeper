"""
Presenter приложения bookkeeper
"""

from typing import Any
from datetime import datetime
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.main_view import MainWindow
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class Bookkeeper:
    """
    Presenter приложения
    """

    def __init__(self, view: MainWindow,
                 cat_repo: SQLiteRepository[Any],
                 exp_repo: SQLiteRepository[Any],
                 bud_repo: SQLiteRepository[Any]) -> None:
        self.view = view
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo

        self.cat_data = self.cat_repo.get_all()
        self.exp_data = self.exp_repo.get_all()
        self.bud_data = self.bud_repo.get_all()

        self.view.on_expense_add_button_clicked(
            self.handle_expense_add_button_clicked)
        self.view.on_budget_item_changed(
            self.handle_budget_item_changed)
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked)
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked)
        self.view.on_category_add_button_clicked(
            self.handle_category_add_button_clicked)
        self.view.on_category_delete_button_clicked(
            self.handle_category_delete_button_clicked)

    def show(self) -> None:
        """Показ главного окна"""
        self.view.show()
        self.view.set_category_dropdown(self.cat_data)
        self.view.set_expense_table(self.exp_data, self.cat_data)
        self.view.set_budget_table(self.exp_data, self.bud_data)

    def handle_expense_add_button_clicked(self) -> None:
        """Обработчик нажатия кнопки Добавить трату"""
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        if amount is None:
            self.view.drop_expense_input()
            return
        comment = self.view.get_comment()
        if comment is None:
            comment = ''
        date = self.view.get_datetime()
        if date is not None:
            exp = Expense(amount=amount, category=cat_pk, comment=comment,
                          expense_date=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        else:
            exp = Expense(amount=amount, category=cat_pk, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
        self.update_budget_data()
        self.view.drop_expense_input()

    def handle_category_edit_button_clicked(self) -> None:
        """Обработчик нажатия на кнопку Редактировать категории"""
        self.view.open_category_window()
        self.cat_data = self.cat_repo.get_all()
        self.view.set_category_table(self.cat_data)
        self.view.set_parent_dropdown(self.cat_data)

    def handle_expense_delete_button_clicked(self, pk: int) -> None:
        """Обработчик нажатия на кнопку Удалить трату"""
        self.exp_repo.delete(pk)
        self.update_expense_data()
        self.update_budget_data()

    def handle_category_delete_button_clicked(self, pk: int) -> None:
        """Обработчик нажатия на кнопку Удалить категорию"""
        cat = self.cat_repo.get(pk)
        if not cat:
            raise KeyError('Cannot find category to delete')
        childs = self.cat_repo.get_all({"parent": pk})
        expenses = self.exp_repo.get_all({"category": pk})
        if cat.parent:
            for child in childs:
                child.parent = cat.parent
                self.cat_repo.update(child)
            for exp in expenses:
                exp.category = cat.parent
                self.exp_repo.update(exp)
        else:
            for exp in expenses:
                self.exp_repo.delete(exp.pk)
            for child in childs:
                child.parent = None
                self.cat_repo.update(child)
            self.update_budget_data()
        self.cat_repo.delete(pk)
        self.update_expense_data()
        self.update_category_data()

    def handle_budget_item_changed(self, item: Any) -> None:
        """Обработчик изменения значения ячеек бюджета"""
        budget = [item.data(1), item.data(0)]
        if budget[0] is not None:
            obj = self.bud_repo.get(budget[0])
            # может приходить "ложный" сигнал от itemChanged при построении таблицы
            if obj.amount == budget[1]:
                return
            obj.amount = budget[1]
            self.bud_repo.update(obj)
            self.bud_data = self.bud_repo.get_all()
            self.exp_data = self.exp_repo.get_all()
            self.view.set_budget_table(self.exp_data, self.bud_data)

    def handle_category_add_button_clicked(self) -> None:
        """Обработчик нажатия на кнопку Добавления категории"""
        cat_name = self.view.get_added_category_name()
        parent_pk = self.view.get_selected_category_parent()
        if cat_name == '':
            return
        if parent_pk == -1:
            cat_new = Category(name=cat_name)
        else:
            cat_new = Category(name=cat_name, parent=parent_pk)
        self.cat_repo.add(cat_new)
        self.update_category_data()

    def update_expense_data(self) -> None:
        """Обновление таблицы трат"""
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = self.cat_repo.get_all()
        self.view.set_expense_table(self.exp_data, self.cat_data)

    def update_budget_data(self) -> None:
        """Обновление таблицы бюджета"""
        self.bud_data = self.bud_repo.get_all()
        self.exp_data = self.exp_repo.get_all()
        self.view.set_budget_table(self.exp_data, self.bud_data)

    def update_category_data(self) -> None:
        """Обновление таблицы категорий"""
        self.cat_data = self.cat_repo.get_all()
        self.view.set_category_table(self.cat_data)
        self.view.set_parent_dropdown(self.cat_data)
        self.view.set_category_dropdown(self.cat_data)
