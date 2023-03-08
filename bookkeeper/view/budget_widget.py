from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets


def set_data(table, data: list[list[str]]):
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            table.setItem(
                i, j,
                QtWidgets.QTableWidgetItem(x.capitalize())
            )


class BudgetWidget(QtWidgets.QTableWidget):
    data = [["700", "1000"],
            ["6000", "3000"],
            ["25000", "3500"], ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        text = QtWidgets.QLabel("Бюджет")
        layout.addWidget(text)

        budget_table = QtWidgets.QTableWidget(2, 3)
        budget_table.setColumnCount(2)
        budget_table.setRowCount(3)
        budget_table.setHorizontalHeaderLabels(
            "Сумма Бюджет".split()
        )
        budget_table.setVerticalHeaderLabels(
            "День Неделя Месяц".split()
        )

        header = budget_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)

        budget_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        set_data(budget_table, self.data)

        layout.addWidget(budget_table)
        self.setLayout(layout)
