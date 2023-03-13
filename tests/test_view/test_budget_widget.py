from bookkeeper.view.budget_widget import BudgetWidget

amounts = {1: 100, 7: 2000, 30: 4000}
limits = {1: [1, 200], 7: [2, 1000], 30: [3, 3000]}


def test_create_widget(qtbot):
    widget = BudgetWidget()
    qtbot.addWidget(widget)
    widget.set_budget_table(amounts, limits)
    for i, (key, val) in enumerate(limits.items()):
        print(f"i={i} key={key} val={val}")
        amount = amounts[key]
        limit = val[1]
        pk = val[0]
        diff = int(abs(amount - limit))
        remain = f"Перерасход на {diff}" if amount > limit else str(diff)
        assert widget.budget_table.item(i, 0).text() == str(amount)
        assert widget.budget_table.item(i, 1).text() == str(limit)
        assert widget.budget_table.item(i, 2).text() == remain
        assert widget.budget_table.item(i, 1).data(1) == pk
