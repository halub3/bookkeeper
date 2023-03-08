from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets

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
        print(exp_data)
        print('Cat dict')
        print(cat_dict)
        print(cat_dict.keys())
        exp_data_list = []
        for d in exp_data:
            print(type(d.category))
            if d.category not in cat_dict.keys():
                raise ValueError(f"Cannot find category wit ID {d.category}")
            exp_data_list.append([d.expense_date, str(d.amount), cat_dict[d.category], d.comment])
        print(exp_data_list)
        self.expense_widget.set_expense_table(exp_data_list)

    def update_expense_data(self, data):
        self.expense_widget.set_expense_table(data)

    def on_expense_add_button_clicked(self, slot):
        self.button_widget.add_button.clicked.connect(slot)

    def get_selected_cat(self):
        return self.button_widget.get_selected_cat()

    def get_amount(self):
        return self.button_widget.get_amount()

    def get_comment(self):
        return self.button_widget.get_comment()

    def get_datetime(self):
        return self.button_widget.get_datetime()


