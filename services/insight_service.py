from statistics import variance
from collections import defaultdict
from datetime import datetime, timedelta

from db.db_utils import (
    fetch_daily_completion_rate,
    fetch_logs_for_habit
)
from services.consistency_service import get_consistency_percentage


def generate_global_trend_insight(min_days=14, min_change_pct=8):
    recent = fetch_daily_completion_rate(days=min_days)
    if len(recent) < min_days:
        return None

    first_half = recent[:min_days // 2]
    second_half = recent[min_days // 2:]

    def avg_rate(rows):
        return sum(r[1] / r[2] for r in rows) / len(rows)

    first_avg = avg_rate(first_half)
    second_avg = avg_rate(second_half)

    diff_pct = (second_avg - first_avg) * 100

    if abs(diff_pct) < min_change_pct:
        return None

    if diff_pct > 0:
        return "📈 Your overall habit completion has meaningfully improved recently."
    else:
        return "📉 Your overall habit completion has meaningfully declined recently."



def generate_weekday_weekend_insight(min_points=6):
    rows = fetch_daily_completion_rate(days=30)
    if not rows:
        return None

    weekday, weekend = [], []

    for date_str, completed, total in rows:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        rate = completed / total

        if date.weekday() < 5:
            weekday.append(rate)
        else:
            weekend.append(rate)

    if len(weekday) < min_points or len(weekend) < min_points:
        return None

    weekday_avg = sum(weekday) / len(weekday)
    weekend_avg = sum(weekend) / len(weekend)

    if abs(weekday_avg - weekend_avg) < 0.1:
        return None

    if weekday_avg > weekend_avg:
        return "📅 You tend to be more consistent on weekdays than weekends."
    else:
        return "📅 You tend to be more consistent on weekends than weekdays."


def generate_habit_stability_insight(habit_id, habit_name, min_logs=10):
    logs = fetch_logs_for_habit(habit_id)
    if len(logs) < min_logs:
        return None

    values = [status for _, status in logs[-30:]]

    try:
        v = variance(values)
    except:
        return None

    if v < 0.08:
        return f"🧘 {habit_name} is very stable."
    elif v < 0.2:
        return f"⚖️ {habit_name} shows moderate variability."
    elif v < 0.35:
        return f"🌊 {habit_name} is inconsistent."
    else:
        return f"🌪️ {habit_name} is highly volatile."
