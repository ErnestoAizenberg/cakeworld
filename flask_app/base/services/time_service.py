from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pytz


class TimeService:
    @staticmethod
    def utc_to_msc(utc_dt: datetime) -> datetime:
        """Конвертирует время из UTC в московское время."""
        utc_zone = pytz.utc
        msc_zone = pytz.timezone("Europe/Moscow")
        return utc_dt.astimezone(msc_zone)

    @staticmethod
    def current_msc_time() -> datetime:
        """Возвращает текущее московское время."""
        return datetime.now(pytz.timezone("Europe/Moscow"))


def pluralize_seconds(seconds: int) -> str:
    if seconds % 10 == 1 and seconds % 100 != 11:
        return f"{seconds} секунда назад"
    elif seconds % 10 in [2, 3, 4] and not (11 <= seconds % 100 <= 14):
        return f"{seconds} секунды назад"
    else:
        return f"{seconds} секунд назад"


def pluralize_minutes(minutes: int) -> str:
    if minutes % 10 == 1 and minutes % 100 != 11:
        return f"{minutes} минута назад"
    elif minutes % 10 in [2, 3, 4] and not (11 <= minutes % 100 <= 14):
        return f"{minutes} минуты назад"
    else:
        return f"{minutes} минут назад"


def pluralize_hours(hours: int) -> str:
    if hours % 10 == 1 and hours % 100 != 11:
        return f"{hours} час назад"
    elif hours % 10 in [2, 3, 4] and not (11 <= hours % 100 <= 14):
        return f"{hours} часа назад"
    else:
        return f"{hours} часов назад"


def pluralize_days(days: int) -> str:
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день назад"
    elif days % 10 in [2, 3, 4] and not (11 <= days % 100 <= 14):
        return f"{days} дня назад"
    else:
        return f"{days} дней назад"


def pluralize_months(months: int) -> str:
    if months % 10 == 1 and months % 100 != 11:
        return f"{months} месяц назад"
    elif months % 10 in [2, 3, 4] and not (11 <= months % 100 <= 14):
        return f"{months} месяца назад"
    else:
        return f"{months} месяцев назад"


def pluralize_years(years: int) -> str:
    if years % 10 == 1 and years % 100 != 11:
        return f"{years} год назад"
    elif years % 10 in [2, 3, 4] and not (11 <= years % 100 <= 14):
        return f"{years} года назад"
    else:
        return f"{years} лет назад"


def time_ago(dt: datetime) -> str:
    """Возвращает строку, указывающую, как давно было создано сообщение."""
    # Приведем dt к тому же часовому поясу, что и now, если dt не содержит временной зоны
    if dt.tzinfo is None:
        dt = pytz.timezone("Europe/Moscow").localize(
            dt
        )  # Создаем offset-aware datetime

    now = datetime.now(pytz.timezone("Europe/Moscow"))
    delta = now - dt

    if delta < timedelta(minutes=1):
        return pluralize_seconds(delta.seconds)
    elif delta < timedelta(hours=1):
        return pluralize_minutes(delta.seconds // 60)
    elif delta < timedelta(days=1):
        return pluralize_hours(delta.seconds // 3600)
    elif delta < timedelta(days=30):
        return pluralize_days(delta.days)
    elif delta < timedelta(days=365):
        return pluralize_months(delta.days // 30)
    else:
        return pluralize_years(delta.days // 365)
