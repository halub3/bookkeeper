from bookkeeper.view.category_window import CategoryWindow


test_data = [{"pk": 1, "name": "cat1", "parent": "cat2"},
             {"pk": 2, "name": "cat3", "parent": "cat4"}]


def test_init_category_window(qtbot):
    window = CategoryWindow()
    assert window.category_table.columnCount() == 3
    assert window.category_label.text() == 'Имя категории'
    assert window.parent_label.text() == 'Родитель категории'
    assert window.add_button.text() == 'Добавить'
    assert window.windowTitle() == 'Редактировать категории'


def test_set_category_table(qtbot):
    window = CategoryWindow()
    qtbot.addWidget(window)
    window.set_category_table(test_data, len(test_data))
    assert window.category_table.rowCount() == len(test_data)
    for i, row in enumerate(test_data):
        assert window.category_table.item(i, 1).text() == row["name"].capitalize()
        assert window.category_table.item(i, 2).text() == row["parent"].capitalize()


def test_set_parent_dropdown(qtbot):
    window = CategoryWindow()
    qtbot.addWidget(window)
    data = [[1, 't1'], [2, 't2'], [3, 't3']]
    window.set_parent_dropdown(data)
    inserted = [window.parent_dropdown.itemText(i) for i in range(window.parent_dropdown.count())]
    correct = ["-"] + [d[1].capitalize() for d in data]
    assert inserted == correct


def test_get_category_name(qtbot):
    window = CategoryWindow()
    qtbot.addWidget(window)
    data = "test_name"
    qtbot.keyClicks(window.category_label_edit, data)
    assert window.category_label_edit.text() == data
    assert window.get_category_name() == data


def test_get_selected_parent(qtbot):
    window = CategoryWindow()
    qtbot.addWidget(window)
    data = [[1, 't1'], [2, 't2'], [3, 't3']]
    window.set_parent_dropdown(data)
    qtbot.keyClicks(window.parent_dropdown, data[1][1].capitalize())
    assert window.parent_dropdown.itemText(window.parent_dropdown.currentIndex()) == data[1][1].capitalize()
    assert window.get_selected_parent() == data[1][0]
