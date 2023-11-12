from datetime import datetime, timedelta

import pytz


def is_same_date(date1: datetime, date2: datetime):
    return date1.date() == date2.date()


def get_yesterday_date(timezone) -> datetime:
    return datetime.now(timezone) - timedelta(days=1)


def get_current_time(timezone) -> datetime:
    return datetime.now(timezone)


def get_timezone(timezonestr):
    return pytz.timezone(timezonestr)
