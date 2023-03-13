from datetime import datetime
from bookkeeper.view.button_widget import ButtonWidget


def test_init_button_widget(qtbot):
    widget = ButtonWidget()
    data = datetime.now()
    data = data.strftime("%Y-%m-%d %H:%M:%S")
    assert widget.datetime_label_edit.text() == data
    assert widget.edit_button.text() == "Редактировать"
    assert widget.add_button.text() == "Добавить"


def test_set_category_dropdown(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data = [[1, 't1'], [2, 't2'], [3, 't3']]
    widget.set_category_dropdown(data)
    inserted = [widget.category_dropdown.itemText(i) for i in range(widget.category_dropdown.count())]
    correct = [d[1].capitalize() for d in data]
    assert inserted == correct


def test_get_amount(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data = int(123)
    qtbot.keyClicks(widget.amount_line_edit, str(data))
    assert widget.amount_line_edit.text() == str(data)
    assert widget.get_amount() == data


def test_error_get_amount(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data = 'text'
    qtbot.keyClicks(widget.amount_line_edit, data)
    assert widget.amount_line_edit.text() == data
    assert widget.get_amount() is None


def test_get_selected_cat(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data = [[1, 't1'], [2, 't2'], [3, 't3']]
    widget.set_category_dropdown(data)
    qtbot.keyClicks(widget.category_dropdown, data[2][1].capitalize())
    assert widget.category_dropdown.itemText(widget.category_dropdown.currentIndex()) == data[2][1].capitalize()
    assert widget.get_selected_cat() == data[2][0]


def test_get_comment(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data = 'text'
    qtbot.keyClicks(widget.comment_label_edit, data)
    assert widget.comment_label_edit.text() == data
    assert widget.get_comment() == data


def test_get_comment_empty(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data = ''
    qtbot.keyClicks(widget.comment_label_edit, data)
    assert widget.comment_label_edit.text() == data
    assert widget.get_comment() is None


def test_get_datetime(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    data_d = datetime.now()
    data = data_d.strftime("%Y-%m-%d %H:%M:%S")
    qtbot.keyClicks(widget.datetime_label_edit, data)
    returned = datetime.strptime(widget.get_datetime(), "%Y-%m-%d %H:%M:%S")
    returned = returned.strftime("%Y-%m-%d %H:%M")
    data = data_d.strftime("%Y-%m-%d %H:%M")
    assert returned == data


def test_drop_input(qtbot):
    widget = ButtonWidget()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.amount_line_edit, '100')
    qtbot.keyClicks(widget.comment_label_edit, 'comment')
    widget.drop_input()
    assert widget.comment_label_edit.text() == ''
    assert widget.amount_line_edit.text() == ''
    assert widget.get_amount() is None
    assert widget.get_comment() is None
