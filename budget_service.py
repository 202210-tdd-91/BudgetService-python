from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta


class Budget:
    def __init__(self, yearMonth, amount):
        self.yearMonth = yearMonth
        self.amount = amount


class BudgetsInterface:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        budget = Budget("202210", 3100)
        return [budget]


class BudgetService:
    def __init__(self):
        budget_interface = BudgetsInterface()
        self.budgets = budget_interface.get_all()

    # '20220828' '20221005'
    def query(self, start: datetime, end: datetime) -> Decimal:
        if start > end:
            return 0

        month_delta = (end.month - start.month) + (end.year - start.year) * 12

        if month_delta == 0:
            return self.get_budget_by_partial_month(start, end)

        else:
            total_budget = 0

            current = start
            # current = start + relativedelta(months=+1)
            while current < end.replace(day=1) + relativedelta(months=+1):
                if current.strftime("%Y%m") == start.strftime("%Y%m"):
                    total_budget += self.get_budget_by_month_start(start)
                elif current.strftime("%Y%m") == end.strftime("%Y%m"):
                    total_budget += self.get_budget_by_month_end(end)
                else:
                    total_budget += self.get_budget_by_full_month(current)
                current = current + relativedelta(months=+1)

            # total_budget += self.get_budget_by_month_end(end)
            return total_budget

    def get_budget_by_month_start(self, start: datetime):
        month_budget = self.get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return month_budget / days_of_month * days

    def get_budget_by_month_end(self, end: datetime):
        month_budget = self.get_month_budget(end)
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return month_budget / days_of_month * days

    def get_budget_by_full_month(self, date: datetime) -> Decimal:
        return self.get_month_budget(date)

    def get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return month_budget / days_of_month * days

    def get_month_budget(self, date: datetime) -> int:
        for i in self.get_budgets():
            if i.yearMonth == date.strftime("%Y%m"):
                return i.amount

        return 0

    def get_budgets(self):
        pass
