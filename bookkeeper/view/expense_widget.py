from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets


class ExpenseWidget(QtWidgets.QTableWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        text = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(text)

        self.expenses_table = QtWidgets.QTableWidget(4, 20)
        self.expenses_table.setColumnCount(4)
        self.expenses_table.setRowCount(20)
        self.expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split()
        )

        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

        self.expenses_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()

        layout.addWidget(self.expenses_table)
        self.setLayout(layout)

    def set_expense_table(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )



