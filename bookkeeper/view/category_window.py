from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from bookkeeper.view.button_widget import RowButton


class CategoryWindow(QtWidgets.QMainWindow):
    delete_signal = QtCore.Signal(int)
    horizontal_labels = "# Название Родитель"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Редактировать категории')
        self.setFixedSize(500, 700)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QtWidgets.QLabel("Категории"))

        self.category_table = QtWidgets.QTableWidget(3, 10)
        self.category_table.setColumnCount(3)
        self.category_table.setRowCount(10)
        self._set_horizontal_labels(self.horizontal_labels)

        header = self.category_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.category_table.verticalHeader().hide()
        layout.addWidget(self.category_table)

        self.category_label = QtWidgets.QLabel('Имя категории')
        self.category_label_edit = QtWidgets.QLineEdit()

        self.parent_label = QtWidgets.QLabel('Родитель категории')
        self.parent_dropdown = QtWidgets.QComboBox()

        self.add_button = QtWidgets.QPushButton("Добавить")

        self.addition_layout = QtWidgets.QGridLayout()
        self.addition_layout.addWidget(self.category_label, 0, 0)
        self.addition_layout.addWidget(self.category_label_edit, 0, 1)
        self.addition_layout.addWidget(self.parent_label, 1, 0)
        self.addition_layout.addWidget(self.parent_dropdown, 1, 1)
        self.addition_layout.addWidget(self.add_button, 2, 0)
        widget = QWidget()
        widget.setLayout(self.addition_layout)
        layout.addWidget(widget)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def _set_horizontal_labels(self, data: list[str]) -> None:
        self.category_table.setHorizontalHeaderLabels(data.split())

    def set_category_table(self, data: list[dict], size: int) -> None:
        self.category_table.clear()
        self.category_table.setRowCount(size)
        self._set_horizontal_labels(self.horizontal_labels)
        for i, row in enumerate(data):
            button = RowButton(row["pk"], self.delete_signal, "Delete")
            self.category_table.setCellWidget(i, 0, button)
            self.category_table.setItem(i, 1, QtWidgets.QTableWidgetItem(row["name"].capitalize()))
            self.category_table.setItem(i, 2, QtWidgets.QTableWidgetItem(row["parent"].capitalize()))

    def set_parent_dropdown(self, data) -> None:
        self.parent_dropdown.clear()
        self.parent_dropdown.addItem('-', -1)
        for tup in data:
            self.parent_dropdown.addItem(tup[1].capitalize(), tup[0])

    def get_category_name(self) -> str:
        return self.category_label_edit.text()

    def get_selected_parent(self) -> int:
        return int(self.parent_dropdown.itemData(self.parent_dropdown.currentIndex()))


