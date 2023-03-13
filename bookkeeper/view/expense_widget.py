"""
GUI таблицы трат
"""

from typing import Any
from PySide6 import QtCore, QtWidgets
from bookkeeper.view.button_widget import RowButton


class ExpenseWidget(QtWidgets.QTableWidget):
    """
    Виджет трат
    """
    delete_signal = QtCore.Signal(int)
    horizontal_labels = "# Дата Сумма Категория Комментарий"

    def __init__(self) -> None:
        super().__init__()

        self.data: list[Any] = []
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(self.label)

        self.expenses_table = QtWidgets.QTableWidget()
        self.expenses_table.setColumnCount(5)

        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.expenses_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()

        layout.addWidget(self.expenses_table)
        self.setLayout(layout)

    def _set_horizontal_labels(self, data: str) -> None:
        self.expenses_table.setHorizontalHeaderLabels(data.split())

    def set_expense_table(self, data: list[dict[str, Any]], size: int) -> None:
        """Заполнить таблицу трат"""
        self.data = data
        self.data.sort(key=lambda d: d["expense_date"], reverse=True)
        self.expenses_table.clear()
        self.expenses_table.setRowCount(size)
        self._set_horizontal_labels(self.horizontal_labels)
        row: Any
        for i, row in enumerate(self.data):
            button = RowButton(row["pk"], self.delete_signal, "Delete")
            self.expenses_table.setCellWidget(i, 0, button)

            item = QtWidgets.QTableWidgetItem(row["expense_date"])
            self.expenses_table.setItem(i, 1, item)

            item = QtWidgets.QTableWidgetItem(str(row["amount"]))
            self.expenses_table.setItem(i, 2, item)

            item = QtWidgets.QTableWidgetItem(row["category"].capitalize())
            self.expenses_table.setItem(i, 3, item)

            item = QtWidgets.QTableWidgetItem(row["comment"])
            self.expenses_table.setItem(i, 4, item)
