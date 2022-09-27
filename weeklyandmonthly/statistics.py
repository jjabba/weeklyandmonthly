##
# This module calculates the averages for past weeks and months.
#
# Note on timezones.
# The bounds used to partition data into weeks and months defaults to utc.
#

from dataclasses import dataclass
import datetime

from calendar import monthrange
from tokenize import Number
from abc import ABC, abstractmethod

class DataPoint(ABC):
    @abstractmethod
    def point_in_time(self) -> datetime:
        pass

    @abstractmethod
    def value(self) -> Number:
        pass


class MonthlyAndWeeklyStatistics:
    def __init__(self, start, end, tzinfo=datetime.timezone.utc, formula='avg') -> None:
        self.start = start
        self.end = end
        self.target_tz = tzinfo
        self.stats = {}
        self.formula = {
            'avg': self.average,
            'sum': self.sum,
            'cnt': self.count
        }[formula]
        self.fully_encompassed_weeks_in_target_tz(start.astimezone(self.target_tz), end.astimezone(self.target_tz))
        self.fully_encompassed_months_in_target_tz(start.astimezone(self.target_tz), end.astimezone(self.target_tz))

    def fully_encompassed_weeks_in_target_tz(self, start, end):
        start_of_monday = MonthlyAndWeeklyStatistics.first_monday(start)
        delta = datetime.timedelta(weeks=1, microseconds=-1)

        while (start_of_monday + delta) <= end:
            key = MonthlyAndWeeklyStatistics.week_key(start_of_monday)
            start_of_monday = start_of_monday + datetime.timedelta(weeks=1)
            self.stats[key] = (0, 0)

    def fully_encompassed_months_in_target_tz(self, start, end):
        start_of_month = MonthlyAndWeeklyStatistics.first_moment_of_month(succeeding=start)
        end_of_month = MonthlyAndWeeklyStatistics.last_moment_of_month(start_of_month)

        while end_of_month <= end:
            key = MonthlyAndWeeklyStatistics.month_key(start_of_month)
            self.stats[key] = (0, 0)
            start_of_month = MonthlyAndWeeklyStatistics.first_moment_of_month(end_of_month)
            end_of_month = MonthlyAndWeeklyStatistics.last_moment_of_month(start_of_month)

    def consider(self, datapoint):
        t = datapoint.point_in_time().astimezone(self.target_tz)
        month_key = MonthlyAndWeeklyStatistics.month_key(t)
        week_key = MonthlyAndWeeklyStatistics.week_key(t)

        value = datapoint.value()

        if week_key in self.stats:
            (sum, count) = self.stats[week_key]
            self.stats[week_key] = (sum + value, count + 1)

        if month_key in self.stats:
            (sum, count) = self.stats[month_key]
            self.stats[month_key] = (sum + value, count + 1)

    def past_weeks(self, nbr_weeks=5):
        return sorted([((y, unit, w), self.formula(s, n)) for ((y, unit, w), (s, n)) in self.stats.items() if 'w' == unit])[-nbr_weeks:]

    def past_months_this_year(self):
        year = datetime.datetime.now(self.target_tz).year
        return sorted([((y, unit, m), self.formula(s, n)) for ((y, unit, m), (s, n)) in self.stats.items() if year == y and unit == 'm'])

    @staticmethod
    def first_monday(succeeding):
        day_nbr = succeeding.weekday()
        if day_nbr == 0 and succeeding.time() == datetime.time.min:
            return succeeding
        # otherwise ffwd
        monday = (succeeding + datetime.timedelta(days=(7 - day_nbr))).date()
        return datetime.datetime.combine(monday, datetime.time.min, tzinfo=succeeding.tzinfo)

    @staticmethod
    def first_moment_of_month(succeeding):
        start_of_month = datetime.datetime.combine(succeeding.replace(day=1).date(), datetime.time.min, tzinfo=succeeding.tzinfo)
        if start_of_month >= succeeding:
            return start_of_month
        # otherwise ffwd
        year = succeeding.year if succeeding.month < 12 else succeeding.year + 1
        first = datetime.date(year, (succeeding.month % 12 + 1), 1)
        return datetime.datetime.combine(first, datetime.time.min, tzinfo=succeeding.tzinfo)

    @staticmethod
    def last_moment_of_month(succeeding):
        (_, last_day) = monthrange(succeeding.year, succeeding.month)
        return datetime.datetime.combine(succeeding.replace(day=last_day).date(), datetime.time.max, tzinfo=succeeding.tzinfo)

    @staticmethod
    def average(sum, cnt, decimals=2):
        return round(sum/float(cnt), 2) if cnt else 0

    @staticmethod
    def sum(sum, _cnt, decimals=2):
        return round(float(sum), 2)

    @staticmethod
    def count(sum, cnt, decimals=2):
        return round(float(cnt), 2)

    @staticmethod
    def month_key(dt):
        return (dt.year, 'm', dt.month)

    @staticmethod
    def week_key(dt):
         return (dt.year, 'w', int(dt.strftime("%V")))
