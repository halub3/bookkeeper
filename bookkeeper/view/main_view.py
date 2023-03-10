from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from datetime import datetime

from bookkeeper.view.expense_widget import ExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.button_widget import ButtonWidget
from bookkeeper.view.category_window import CategoryWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
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

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def set_category_dropdown(self, data):
        cat_data_list = [[str(d.pk), d.name] for d in data]
        self.button_widget.set_category_dropdown(cat_data_list)

    def set_parent_dropdown(self, data):
        cat_data_list = [[str(d.pk), d.name] for d in data]
        self.category_window.set_parent_dropdown(cat_data_list)

    def set_expense_table(self, exp_data, cat_data):
        expense_size = len(exp_data)
        cat_dict = {d.pk: d.name for d in cat_data}
        exp_data_list = []
        for d in exp_data:
            if d.category not in cat_dict.keys():
                raise ValueError(f"Cannot find category wit ID {d.category}")
            exp_data_list.append({"pk": d.pk,
                                  "expense_date": d.expense_date,
                                  "amount": d.amount,
                                  "category": cat_dict[d.category],
                                  "comment": d.comment,
                                  })
        self.expense_widget.set_expense_table(exp_data_list, expense_size)

    def set_budget_table(self, exp_data, bud_data):
        limit_dict = {d.period: [d.pk, d.amount] for d in bud_data}
        amount_dict = {1: 0, 7: 0, 30: 0}
        for data in exp_data:
            date = datetime.strptime(data.expense_date, '%Y-%m-%d %H:%M:%S')
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

    def set_category_table(self, cat_data):
        cat_size = len(cat_data)
        cat_dict = {d.pk: d.name for d in cat_data}
        cat_list = []
        for row in cat_data:
            cat_list.append({"pk": row.pk,
                             "name": row.name,
                             "parent": cat_dict[row.parent] if row.parent in cat_dict else '-'})
        self.category_window.set_category_table(cat_list, cat_size)

    def on_expense_add_button_clicked(self, slot):
        self.button_widget.add_button.clicked.connect(slot)

    def on_category_edit_button_clicked(self, slot):
        return self.button_widget.edit_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot):
        return self.expense_widget.delete_signal.connect(slot)

    def on_category_delete_button_clicked(self, slot):
        return self.category_window.delete_signal.connect(slot)

    def on_category_add_button_clicked(self, slot):
        return self.category_window.add_button.clicked.connect(slot)

    def on_budget_item_changed(self, slot):
        self.budget_widget.budget_table.itemChanged.connect(slot)

    def get_selected_cat(self) -> int:
        return int(self.button_widget.get_selected_cat())

    def get_amount(self):
        return self.button_widget.get_amount()

    def get_comment(self):
        return self.button_widget.get_comment()

    def get_datetime(self):
        return self.button_widget.get_datetime()

    def get_changed_budget(self, item):
        return self.budget_widget.get_changed_budget(item)

    def open_category_window(self):
        self.category_window.show()

    def drop_expense_input(self):
        self.button_widget.drop_input()

    def get_added_category_name(self):
        return self.category_window.get_category_name()

    def get_selected_category_parent(self):
        return self.category_window.get_selected_parent()



