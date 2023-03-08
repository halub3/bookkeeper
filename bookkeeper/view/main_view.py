from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from datetime import datetime

from bookkeeper.view.expense_widget import ExpenseWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.button_widget import ButtonWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bookkeeper")
        self.setFixedSize(700, 700)

        self.expense_widget = ExpenseWidget()
        self.budget_widget = BudgetWidget()
        self.button_widget = ButtonWidget()

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

    def set_expense_table(self, exp_data, cat_data):
        cat_dict = {str(d.pk): d.name for d in cat_data}
        exp_data_list = []
        for d in exp_data:
            if d.category not in cat_dict.keys():
                raise ValueError(f"Cannot find category wit ID {d.category}")
            exp_data_list.append([d.expense_date, str(d.amount), cat_dict[d.category], d.comment])
        self.expense_widget.set_expense_table(exp_data_list)

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

    def update_expense_data(self, data):
        self.expense_widget.set_expense_table(data)

    def on_expense_add_button_clicked(self, slot):
        self.button_widget.add_button.clicked.connect(slot)

    def on_budget_item_changed(self, slot):
        self.budget_widget.budget_table.itemChanged.connect(slot)

        # self.budget_widget.budget_table.currentItemChanged.connect(slot)

    def get_selected_cat(self):
        return self.button_widget.get_selected_cat()

    def get_amount(self):
        return self.button_widget.get_amount()

    def get_comment(self):
        return self.button_widget.get_comment()

    def get_datetime(self):
        return self.button_widget.get_datetime()

    def get_changed_budget(self, item):
        return self.budget_widget.get_changed_budget(item)


