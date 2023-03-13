"""
GUI окна просмотра и редактирования категорий
"""

from typing import Any
from PySide6 import QtCore, QtWidgets
from bookkeeper.view.button_widget import RowButton


class CategoryWindow(QtWidgets.QMainWindow):
    """
    Окно просмотра и редактирования категорий
    """

    delete_signal = QtCore.Signal(int)
    horizontal_labels = "# Название Родитель"

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Редактировать категории")
        self.setFixedSize(500, 700)

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Категории")
        layout.addWidget(label)

        self.category_table = QtWidgets.QTableWidget()
        self.category_table.setColumnCount(3)

        header = self.category_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.category_table.verticalHeader().hide()
        self.category_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.category_table)

        self.category_label = QtWidgets.QLabel("Имя категории")
        self.category_label_edit = QtWidgets.QLineEdit()

        self.parent_label = QtWidgets.QLabel("Родитель категории")
        self.parent_dropdown = QtWidgets.QComboBox()

        self.add_button = QtWidgets.QPushButton("Добавить")

        self.addition_layout = QtWidgets.QGridLayout()
        self.addition_layout.addWidget(self.category_label, 0, 0)
        self.addition_layout.addWidget(self.category_label_edit, 0, 1)
        self.addition_layout.addWidget(self.parent_label, 1, 0)
        self.addition_layout.addWidget(self.parent_dropdown, 1, 1)
        self.addition_layout.addWidget(self.add_button, 2, 0)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.addition_layout)
        layout.addWidget(widget)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def _set_horizontal_labels(self, data: str) -> None:
        """Установить горизонатльный хэдер в таблице"""
        self.category_table.setHorizontalHeaderLabels(data.split())

    def set_category_table(self, data: list[dict[str, Any]], size: int) -> None:
        """Занести данные имеющихся категорий"""
        self.category_table.clear()
        self.category_table.setRowCount(size)
        self._set_horizontal_labels(self.horizontal_labels)
        for i, row in enumerate(data):
            button = RowButton(row["pk"], self.delete_signal, "Delete")
            self.category_table.setCellWidget(i, 0, button)

            item = QtWidgets.QTableWidgetItem(row["name"].capitalize())
            self.category_table.setItem(i, 1, item)

            item = QtWidgets.QTableWidgetItem(row["parent"].capitalize())
            self.category_table.setItem(i, 2, item)

    def set_parent_dropdown(self, data: list[list[Any]]) -> None:
        """Занести список родителей"""
        self.parent_dropdown.clear()
        self.parent_dropdown.addItem('-', -1)
        for tup in data:
            self.parent_dropdown.addItem(tup[1].capitalize(), tup[0])

    def get_category_name(self) -> str:
        """Получить введенное имя категории"""
        return self.category_label_edit.text()

    def get_selected_parent(self) -> int:
        """Получить выбранного родителя категории"""
        return int(self.parent_dropdown.itemData(self.parent_dropdown.currentIndex()))
