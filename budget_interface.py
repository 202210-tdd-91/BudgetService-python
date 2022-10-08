from typing import List


class Budget:
    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount


class BudgetsInterface:
    budgets = []

    @classmethod
    def get_all(cls) -> List[Budget]:
        return cls.budgets  # implement function to query data from db here

    @classmethod
    def inject_mock_data(cls, budgets) -> None:
        cls.budgets = budgets
