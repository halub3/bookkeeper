from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from datetime import datetime


class RowButton(QtWidgets.QPushButton):
    def __init__(self, item, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
        self.signal = signal
        self.clicked.connect(lambda _: self.signal.emit(self.item))


class ButtonWidget(QtWidgets.QTableWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()

        self.amount_label = QtWidgets.QLabel('Сумма')
        self.amount_line_edit = QtWidgets.QLineEdit()

        self.category_label = QtWidgets.QLabel('Категория')
        self.category_dropdown = QtWidgets.QComboBox()

        self.comment_label = QtWidgets.QLabel('Комментарий')
        self.comment_label_edit = QtWidgets.QLineEdit()

        self.datetime_label = QtWidgets.QLabel('Дата')
        self.datetime_label_edit = QtWidgets.QDateTimeEdit()
        self.datetime_label_edit.setDateTime(datetime.now())
        self.datetime_label_edit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.datetime_label_edit.setCalendarPopup(True)

        self.edit_button = QtWidgets.QPushButton("Редактировать")
        self.add_button = QtWidgets.QPushButton("Добавить")

        self.grid_controls = QtWidgets.QGridLayout()
        self.grid_controls.addWidget(self.amount_label, 0, 0)
        self.grid_controls.addWidget(self.amount_line_edit, 0, 1)
        self.grid_controls.addWidget(self.category_label, 1, 0)
        self.grid_controls.addWidget(self.category_dropdown, 1, 1)
        self.grid_controls.addWidget(self.edit_button, 1, 2)
        self.grid_controls.addWidget(self.comment_label, 2, 0)
        self.grid_controls.addWidget(self.comment_label_edit, 2, 1)
        self.grid_controls.addWidget(self.datetime_label, 3, 0)
        self.grid_controls.addWidget(self.datetime_label_edit, 3, 1)
        self.grid_controls.addWidget(self.add_button, 4, 1)

        widget = QWidget()
        widget.setLayout(self.grid_controls)
        layout.addWidget(widget)
        self.setLayout(layout)

    def set_category_dropdown(self, data):
        self.category_dropdown.clear()
        for tup in data:
            self.category_dropdown.addItem(tup[1].capitalize(), tup[0])

    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())  # TODO: обработка исключений

    def get_selected_cat(self) -> int:
        return int(self.category_dropdown.itemData(self.category_dropdown.currentIndex()))

    def get_comment(self) -> str:
        comment = self.comment_label_edit.text()
        if comment == '':
            return None
        return comment

    def get_datetime(self) -> str:
        return self.datetime_label_edit.text()

    def drop_input(self):
        self.amount_line_edit.clear()
        self.comment_label_edit.clear()



