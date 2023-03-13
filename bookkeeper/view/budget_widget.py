"""
GUI таблицы бюджета
"""

from typing import Any
from PySide6 import QtCore, QtWidgets


class BudgetWidget(QtWidgets.QTableWidget):
    """
    Виджет таблицы бюджета
        Столбец с бюджетом можно править через GUI
    """

    periodMap = {
        0: 1,
        1: 7,
        2: 30,
    }

    def __init__(self) -> None:
        super().__init__()

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
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.budget_table)
        self.setLayout(layout)

    def set_budget_table(self, amounts: dict[int, int], limits: dict[Any, Any]) -> None:
        """Заполнить таблицу бюджета"""
        for idx, step in enumerate([1, 7, 30]):
            item = QtWidgets.QTableWidgetItem(str(amounts[step]))
            self.budget_table.setItem(idx, 0, item)

            item = QtWidgets.QTableWidgetItem(str(limits[step][1]))
            item.setData(1, limits[step][0])
            self.budget_table.setItem(idx, 1, item)

            remain = int(limits[step][1]) - amounts[step]
            if remain < 0:
                item = QtWidgets.QTableWidgetItem('Перерасход на ' + str(abs(remain)))
            else:
                item = QtWidgets.QTableWidgetItem(str(remain))
            self.budget_table.setItem(idx, 2, item)

        self.budget_table.item(0, 0).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(1, 0).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(2, 0).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(0, 2).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(1, 2).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.budget_table.item(2, 2).setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
