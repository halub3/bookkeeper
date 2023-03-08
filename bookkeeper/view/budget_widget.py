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
    periodMap = {
        0: 1,
        1: 7,
        2: 30,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        text = QtWidgets.QLabel("Бюджет")
        layout.addWidget(text)

        self.budget_table = QtWidgets.QTableWidget(3, 3)
        self.budget_table.setColumnCount(3)
        self.budget_table.setRowCount(3)
        self.budget_table.setHorizontalHeaderLabels(
            "Сумма Бюджет Остаток".split()
        )
        self.budget_table.setVerticalHeaderLabels(
            "День Неделя Месяц".split()
        )

        header = self.budget_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)

        # self.budget_table.setEditTriggers(
        #     QtWidgets.QAbstractItemView.NoEditTriggers)

        # set_data(budget_table, self.data)

        layout.addWidget(self.budget_table)
        self.setLayout(layout)

    def set_budget_table(self, amounts, limits) -> None:
        for idx, step in enumerate([1, 7, 30]):
            item = QtWidgets.QTableWidgetItem(str(amounts[step]))
            self.budget_table.setItem(idx, 0, item)

            item = QtWidgets.QTableWidgetItem(str(limits[step][1]))
            item.setData(1, limits[step][0])
            self.budget_table.setItem(idx, 1, item)

            remain = float(limits[step][1]) - amounts[step]
            if remain < 0:
                remain = 'Перерасход на ' + str(abs(remain))
            item = QtWidgets.QTableWidgetItem(str(remain))
            self.budget_table.setItem(idx, 2, item)

        self.budget_table.item(0, 0).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(1, 0).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(2, 0).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(0, 2).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(1, 2).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(2, 2).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)


    def get_changed_budget(self, item):
        return [item.data(1), item.data(0)]

    # def update_budget_item(self, item):
