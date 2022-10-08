from calendar import monthrange
from datetime import datetime
from decimal import Decimal


class Budget:
    def __init__(self, yearMonth, amount):
        self.yearMonth = yearMonth
        self.amount = amount

    def get_days(self):
        return monthrange(int(self.yearMonth[:4]), int(self.yearMonth[-2:]))[1]

    def daily_amount(self):
        return self.amount / self.get_days()

    def get_last_day(self):
        first_day = datetime.strptime(self.yearMonth, '%Y%m').date()
        return datetime(first_day.year, first_day.month, self.get_days())

    def get_first_day(self):
        return datetime.strptime(self.yearMonth, '%Y%m')

    def get_overlapping_amount(self, period):
        another_period = Period(self.get_first_day(), self.get_last_day())
        return self.daily_amount() * period.get_overlapping_days(another_period)


class BudgetsInterface:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        budget = Budget("202210", 3100)
        return [budget]


class Period:
    def __init__(self, start, end) -> None:
        super().__init__()
        self.end = end
        self.start = start

    def get_overlapping_days(self, another_period):
        if self.start > self.end:
            return 0
        overlapping_start = self.start if self.start > another_period.start else another_period.start
        overlapping_end = self.end if self.end < another_period.end else another_period.end
        return (overlapping_end - overlapping_start).days + 1


class BudgetService:
    def __init__(self):
        budget_interface = BudgetsInterface()
        self.budgets = budget_interface.get_all()

    # '20220828' '20221005'
    def query(self, start: datetime, end: datetime) -> Decimal:

        period = Period(start, end)
        return sum(budget.get_overlapping_amount(period) for budget in self.get_budgets())

    def get_budget_by_month_start(self, start: datetime):
        month_budget = self.get_month_budget(start).amount
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return month_budget / days_of_month * days

    def get_budget_by_month_end(self, end: datetime):
        month_budget = self.get_month_budget(end).amount
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return month_budget / days_of_month * days

    def get_budget_by_full_month(self, date: datetime) -> Decimal:
        return self.get_month_budget(date).amount

    def get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.get_month_budget(start).amount
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return month_budget / days_of_month * days

    def get_month_budget(self, date: datetime) -> Budget:
        for i in self.get_budgets():
            if i.yearMonth == date.strftime("%Y%m"):
                return i
                # return i.amount

        return None

    def get_budgets(self):
        pass
