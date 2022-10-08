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
    def query(self, start: datetime, end: datetime) -> Decimal:
        period = Period(start, end)
        return sum(budget.get_overlapping_amount(period) for budget in self.get_budgets())

    def get_budgets(self):
        pass
