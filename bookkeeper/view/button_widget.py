"""
GUI виджета с кнопками изменения/добавления контента
"""

from typing import Any
from PySide6 import QtWidgets, QtCore


class QPushButtonWithSignals(QtWidgets.QPushButton):
    """Искусственный класс для обхода ошибки mypy"""
    clicked: QtCore.Signal


class RowButton(QPushButtonWithSignals):
    """
    Кнопка в ячейке таблицы
    """

    def __init__(self, pk: int, signal: QtCore.SignalInstance, label: str) -> None:
        super().__init__(label)
        self.pk = pk
        self.signal = signal
        self.clicked.connect(lambda _: self.signal.emit(self.pk))


class ButtonWidget(QtWidgets.QTableWidget):
    """
    Виджет кнопок изменения контента главной странцы
        Добавление трат
        Кнопка редактирования категорий
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        amount_label = QtWidgets.QLabel('Сумма')
        self.amount_line_edit = QtWidgets.QLineEdit()

        category_label = QtWidgets.QLabel('Категория')
        self.category_dropdown = QtWidgets.QComboBox()

        comment_label = QtWidgets.QLabel('Комментарий')
        self.comment_label_edit = QtWidgets.QLineEdit()

        datetime_label = QtWidgets.QLabel('Дата')
        self.datetime_label_edit = QtWidgets.QDateTimeEdit()
        self.datetime_label_edit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.datetime_label_edit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.datetime_label_edit.setCalendarPopup(True)

        self.edit_button = QtWidgets.QPushButton("Редактировать")
        self.add_button = QtWidgets.QPushButton("Добавить")

        self.grid_controls = QtWidgets.QGridLayout()
        self.grid_controls.addWidget(amount_label, 0, 0)
        self.grid_controls.addWidget(self.amount_line_edit, 0, 1)
        self.grid_controls.addWidget(category_label, 1, 0)
        self.grid_controls.addWidget(self.category_dropdown, 1, 1)
        self.grid_controls.addWidget(self.edit_button, 1, 2)
        self.grid_controls.addWidget(comment_label, 2, 0)
        self.grid_controls.addWidget(self.comment_label_edit, 2, 1)
        self.grid_controls.addWidget(datetime_label, 3, 0)
        self.grid_controls.addWidget(self.datetime_label_edit, 3, 1)
        self.grid_controls.addWidget(self.add_button, 4, 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.grid_controls)
        layout.addWidget(widget)
        self.setLayout(layout)

    def set_category_dropdown(self, data: list[list[Any]]) -> None:
        """Занести список категорий"""
        self.category_dropdown.clear()
        for tup in data:
            self.category_dropdown.addItem(tup[1].capitalize(), tup[0])

    def get_amount(self) -> int | None:
        """Получить значение суммы добавляемой траты"""
        try:
            ret = int(self.amount_line_edit.text())
        except ValueError:
            ret = None
        return ret

    def get_selected_cat(self) -> int:
        """Получить id категории добавляемой траты"""
        return int(self.category_dropdown.itemData(self.category_dropdown.currentIndex()))

    def get_comment(self) -> str | None:
        """Получить комментарий добавляемой траты"""
        comment = self.comment_label_edit.text()
        if comment == '':
            return None
        return comment

    def get_datetime(self) -> str:
        """Получить дату добавляемой траты"""
        return self.datetime_label_edit.text()

    def drop_input(self) -> None:
        """Сбросить текстовые поля добавляемой траты"""
        self.amount_line_edit.clear()
        self.comment_label_edit.clear()
