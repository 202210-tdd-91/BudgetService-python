from datetime import datetime, timedelta
from decimal import Decimal
from calendar import monthrange
from dateutil.relativedelta import relativedelta

from budget_interface import BudgetsInterface


class BudgetService:
    def __init__(self):
        self.budgets = []

    def query(self, start: datetime, end: datetime) -> Decimal:
        self.budgets = BudgetsInterface.get_all()

        if start > end:
            return Decimal(0)

        month_delta = (end.year - start.year) * 12 + (end.month - start.month)
        if month_delta == 0:
            return self.__get_budget_within_same_month(start, end)
        else:
            return self.__get_budget_across_different_months(start, end, month_delta)

    def __get_budget_within_same_month(self, start, end) -> Decimal:
        return self.__get_partial_month_budget(start, end)

    def __get_budget_across_different_months(self, start, end, month_delta) -> Decimal:
        total_budget = Decimal(0)
        total_budget += self.__get_partial_month_budget_with_start(start)
        for i in range(1, month_delta):
            total_budget += self.__get_entire_month_budget(
                start + relativedelta(months=i)
            )
        total_budget += self.__get_partial_month_budget_with_end(end)
        return total_budget

    def __get_partial_month_budget_with_start(self, start: datetime) -> Decimal:
        end = (
            datetime(start.year, start.month, 1)
            + relativedelta(months=1)
            - timedelta(days=1)
        )
        return self.__get_partial_month_budget(start, end)

    def __get_partial_month_budget_with_end(self, end: datetime) -> Decimal:
        start = datetime(end.year, end.month, 1)
        return self.__get_partial_month_budget(start, end)

    def __get_partial_month_budget(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.__get_entire_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return Decimal(self.__calculate_budget(days, days_of_month, month_budget))

    def __get_entire_month_budget(self, date: datetime) -> int:
        for i in self.budgets:
            if i.year_month == date.strftime("%Y%m"):
                return i.amount
        return 0

    @staticmethod
    def __calculate_budget(days: int, days_of_month: int, month_budget: int) -> float:
        return month_budget / days_of_month * days
