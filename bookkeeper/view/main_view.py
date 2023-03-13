"""
GUI основного окна приложения
"""

from datetime import datetime
from typing import Callable, Any
from PySide6 import QtWidgets

from bookkeeper.view.expense_widget import ExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.button_widget import ButtonWidget
from bookkeeper.view.category_window import CategoryWindow
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class MainWindow(QtWidgets.QMainWindow):
    """
    Окно основого контента:
        Таблица трат
        Таблица бюджета
        Виджет функциональных кнопок
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Bookkeeper")
        self.setFixedSize(700, 700)

        self.expense_widget = ExpenseWidget()
        self.budget_widget = BudgetWidget()
        self.button_widget = ButtonWidget()
        self.category_window = CategoryWindow()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.expense_widget)
        layout.addWidget(self.budget_widget)
        layout.addWidget(self.button_widget)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def set_category_dropdown(self, data: list[Category]) -> None:
        """Установить значения выпадающего списка Категорий"""
        cat_data_list = [[str(d.pk), d.name] for d in data]
        self.button_widget.set_category_dropdown(cat_data_list)

    def set_parent_dropdown(self, data: list[Category]) -> None:
        """Установить значения выпадающего списка родителей Категорий"""
        cat_data_list = [[str(d.pk), d.name] for d in data]
        self.category_window.set_parent_dropdown(cat_data_list)

    def set_expense_table(self, exp_data: list[Expense],
                          cat_data: list[Category]) -> None:
        """Установить значения таблицы трат"""
        expense_size = len(exp_data)
        cat_dict = {d.pk: d.name for d in cat_data}
        exp_data_list = []
        for data in exp_data:
            if data.category not in cat_dict.keys():
                raise ValueError(f"Cannot find category wit ID {data.category}")
            exp_data_list.append({"pk": data.pk,
                                  "expense_date": data.expense_date,
                                  "amount": data.amount,
                                  "category": cat_dict[data.category],
                                  "comment": data.comment,
                                  })
        self.expense_widget.set_expense_table(exp_data_list, expense_size)

    def set_budget_table(self, exp_data: list[Expense], bud_data: list[Budget]) -> None:
        """Установить значения таблицы бюджета"""
        limit_dict = {d.period: [d.pk, d.amount] for d in bud_data}
        amount_dict = {1: 0, 7: 0, 30: 0}
        for data in exp_data:
            date = datetime.strptime(str(data.expense_date), '%Y-%m-%d %H:%M:%S')
            diff_days = (datetime.now() - date).days
            if diff_days == 0:
                amount_dict[1] += data.amount
                amount_dict[7] += data.amount
                amount_dict[30] += data.amount
            elif 0 < diff_days < 7:
                amount_dict[7] += data.amount
                amount_dict[30] += data.amount
            elif diff_days < 30:
                amount_dict[30] += data.amount
        self.budget_widget.set_budget_table(amount_dict, limit_dict)

    def set_category_table(self, cat_data: list[Category]) -> None:
        """Установить значения таблицы категорий"""
        cat_size = len(cat_data)
        cat_dict = {d.pk: d.name for d in cat_data}
        cat_list = []
        for row in cat_data:
            cat_list.append(
                {"pk": row.pk,
                 "name": row.name,
                 "parent": cat_dict[row.parent] if row.parent in cat_dict else '-'}
            )
        self.category_window.set_category_table(cat_list, cat_size)

    def on_expense_add_button_clicked(self, slot: Callable[[], None]) -> None:
        """При нажатии на кнопку Добавить трату"""
        self.button_widget.add_button.clicked.connect(slot)

    def on_category_edit_button_clicked(self, slot: Callable[[], None]) -> None:
        """При нажатии на кнопку Редактировать категории"""
        self.button_widget.edit_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot: Callable[[int], None]) -> None:
        """При нажатии на кнопку Удалить тарту"""
        self.expense_widget.delete_signal.connect(slot)

    def on_category_delete_button_clicked(self, slot: Callable[[int], None]) -> None:
        """При нажатии на кнопку Удалить категории"""
        self.category_window.delete_signal.connect(slot)

    def on_category_add_button_clicked(self, slot: Callable[[], None]) -> None:
        """При нажатии на кнопку Добавить категорию"""
        self.category_window.add_button.clicked.connect(slot)

    def on_budget_item_changed(self, slot: Callable[[Any], None]) -> None:
        """При изменении ячейки таблицы бюджета"""
        self.budget_widget.budget_table.itemChanged.connect(slot)

    def get_selected_cat(self) -> int:
        """Получить id категории добавляемой траты"""
        return int(self.button_widget.get_selected_cat())

    def get_amount(self) -> int | None:
        """Получить введенную сумму добавляемой траты"""
        return self.button_widget.get_amount()

    def get_comment(self) -> str | None:
        """Получить комментарий добавляемой траты"""
        return self.button_widget.get_comment()

    def get_datetime(self) -> str:
        """Получть дату добавляемой траты"""
        return self.button_widget.get_datetime()

    def open_category_window(self) -> None:
        """Открыть окно просмотра категорий"""
        self.category_window.show()

    def drop_expense_input(self) -> None:
        """Сбросить поля добавления траты"""
        self.button_widget.drop_input()

    def get_added_category_name(self) -> str:
        """Получить название добавляемой категории"""
        return self.category_window.get_category_name()

    def get_selected_category_parent(self) -> int:
        """Получить id родителя добавляемой категории"""
        return self.category_window.get_selected_parent()
