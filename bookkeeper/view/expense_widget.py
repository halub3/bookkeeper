from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from bookkeeper.view.button_widget import RowButton


class ExpenseWidget(QtWidgets.QTableWidget):
    delete_signal = QtCore.Signal(int)
    horizontal_labels = "# Дата Сумма Категория Комментарий"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        text = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(text)

        self.expenses_table = QtWidgets.QTableWidget(5, 20)
        self.expenses_table.setColumnCount(5)
        self.expenses_table.setRowCount(20)
        self._set_horizontal_labels(self.horizontal_labels)

        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        self.expenses_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()

        layout.addWidget(self.expenses_table)
        self.setLayout(layout)

    def set_expense_table(self, data: list[dict], size: int):
        data.sort(key=lambda d: d["expense_date"], reverse=True)
        self.expenses_table.clear()
        self.expenses_table.setRowCount(size)
        self._set_horizontal_labels(self.horizontal_labels)
        for i, row in enumerate(data):
            button = RowButton(row["pk"], self.delete_signal, "Delete")
            self.expenses_table.setCellWidget(i, 0, button)
            self.expenses_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row["expense_date"]))
            self.expenses_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row["amount"])))
            self.expenses_table.setItem(i, 3, QtWidgets.QTableWidgetItem(row["category"].capitalize()))
            self.expenses_table.setItem(i, 4, QtWidgets.QTableWidgetItem(row["comment"]))

    def _set_horizontal_labels(self, data):
        self.expenses_table.setHorizontalHeaderLabels(data.split())




