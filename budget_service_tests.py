import unittest
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from budget_service import Budget, BudgetService


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        get_budgets_patcher = patch('budget_service.BudgetService.get_budgets')
        self.fake_get_budgets = get_budgets_patcher.start()
        self.budget_service = BudgetService()
        self.fake_get_budgets.return_value = [Budget("202210", 3100)]

    def test_should_get_full_month_budget_private(self):
        test_date = datetime(2022, 10, 2)
        budget = self.budget_service.get_month_budget(test_date).amount
        self.assertEqual(budget, 3100)

    def test_should_get_partial_month_budget(self):
        start_date = datetime(2022, 10, 2)
        end_date = datetime(2022, 10, 10)
        budget = self.budget_service.get_budget_by_partial_month(start_date, end_date)
        self.assertEqual(budget, 900)

    def test_should_get_partial_month_budget(self):
        start_date = datetime(2022, 10, 2)
        end_date = datetime(2022, 10, 10)
        budget = self.budget_service.get_budget_by_partial_month(start_date, end_date)
        self.assertEqual(budget, 900)

    def test_should_get_full_month_budget(self):
        test_date = datetime(2022, 10, 2)
        budget = self.budget_service.get_budget_by_full_month(test_date)
        self.assertEqual(budget, 3100)

    def test_should_get_budget_by_month_start(self):
        test_date = datetime(2022, 10, 28)
        budget = self.budget_service.get_budget_by_month_start(test_date)
        self.assertEqual(budget, 400)

    def test_should_get_budget_by_month_end(self):
        test_date = datetime(2022, 10, 3)
        budget = self.budget_service.get_budget_by_month_end(test_date)
        self.assertEqual(budget, 300)

    def test_should_be_single_month(self):
        self.given_budgets([Budget("202210", 3100)])
        start_date = datetime(2022, 10, 3)
        end_date = datetime(2022, 10, 5)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(300))

    def given_budgets(self, budgets):
        self.fake_get_budgets.return_value = budgets

    def tearDown(self) -> None:
        patch.stopall()

    def test_should_be_two_months(self):
        self.given_budgets([
            Budget("202210", 3100),
            Budget("202211", 300),
        ])
        start_date = datetime(2022, 10, 28)
        end_date = datetime(2022, 11, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(400 + 30, budget)

    def test_should_be_multiple_months(self):
        self.given_budgets([
            Budget("202210", 3100),
            Budget("202211", 300),
            Budget("202212", 31),
        ])
        start_date = datetime(2022, 10, 28)
        end_date = datetime(2022, 12, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(400 + 300 + 3, budget)


if __name__ == "__main__":
    unittest.main()
