from bookkeeper.models.expense import Expense


class Bookkeeper:

    def __init__(self, view, cat_repo, exp_repo, bud_repo):
        # self.model = model
        self.view = view
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo

        self.cat_data = self.cat_repo.get_all()
        self.exp_data = self.exp_repo.get_all()
        self.bud_data = self.bud_repo.get_all()

        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_budget_item_changed(self.handle_budget_item_changed)

        # self.view.update_expense_data(self.exp_data)
        # self.view.init_category_data(cat_data_list)

    def show(self):
        self.view.show()
        # self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)
        self.view.set_expense_table(self.exp_data, self.cat_data)
        self.view.set_budget_table(self.exp_data, self.bud_data)

    def handle_expense_add_button_clicked(self):
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        if comment is None:
            comment = ''
        datetime = self.view.get_datetime()
        if datetime is not None:
            exp = Expense(amount=amount, category=cat_pk, comment=comment, expense_date=datetime)
        else:
            exp = Expense(amount=amount, category=cat_pk, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
        self.update_budget_data()

    def handle_budget_item_changed(self, item):
        budget = self.view.get_changed_budget(item)
        # print(f"Budget with data {budget[1]} and pk {budget[0]}")
        if budget[0] is not None:
            obj = self.bud_repo.get(budget[0])
            if obj.amount == budget[1]:  # может приходить "ложный" сигнал от itemChanged при построении таблицы
                return
            obj.amount = budget[1]
            self.bud_repo.update(obj)
            self.bud_data = self.bud_repo.get_all()
            self.exp_data = self.exp_repo.get_all()
            self.view.set_budget_table(self.exp_data, self.bud_data)

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        self.view.set_expense_table(self.exp_data, self.cat_data)

    def update_budget_data(self):
        self.bud_data = self.bud_repo.get_all()
        self.exp_data = self.exp_repo.get_all()
        self.view.set_budget_table(self.exp_data, self.bud_data)
