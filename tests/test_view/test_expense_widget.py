from bookkeeper.view.expense_widget import ExpenseWidget

test_data = [{"pk": 1, "expense_date": "2023-03-12 17:08:06", "amount": 100, "category": "Cat1", "comment": "com1"},
             {"pk": 2, "expense_date": "2023-03-11 17:08:06", "amount": 200, "category": "Cat2", "comment": "com2"}]


def test_init_expense_widget(qtbot):
    widget = ExpenseWidget()
    assert widget.expenses_table.columnCount() == 5
    assert widget.label.text() == "Последние расходы"

def test_set_expense_table(qtbot):
    widget = ExpenseWidget()
    qtbot.addWidget(widget)
    widget.set_expense_table(test_data, len(test_data))
    assert widget.data == test_data
    for i, row in enumerate(test_data):
        print(f"i = {i}")
        for j, (key, val) in enumerate(row.items()):
            print(f"j = {j}, key={key}, val={val}")
            if key == "pk":
                assert True
            else:
                assert widget.expenses_table.item(i, j).text() == str(val)


