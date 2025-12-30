from statistics import variance
from collections import defaultdict
from datetime import datetime, timedelta

from db.db_utils import (
    fetch_daily_completion_rate,
    fetch_logs_for_habit
)
from services.consistency_service import get_consistency_percentage


def generate_global_trend_insight():
    recent = fetch_daily_completion_rate(days=7)
    previous = fetch_daily_completion_rate(days=14)

    if len(previous) < 14 or len(recent) < 7:
        return None

    recent_avg = sum(r[1] / r[2] for r in recent[-7:]) / 7
    previous_avg = sum(r[1] / r[2] for r in previous[:7]) / 7

    diff = (recent_avg - previous_avg) * 100

    if diff > 5:
        return "📈 Your overall habit completion improved compared to last week."
    elif diff < -5:
        return "📉 Your overall habit completion declined compared to last week."
    else:
        return "➖ Your overall habit completion is stable week over week."


def generate_weekday_weekend_insight():
    rows = fetch_daily_completion_rate(days=30)
    if not rows:
        return None

    weekday = []
    weekend = []

    for date_str, completed, total in rows:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        rate = completed / total

        if date.weekday() < 5:
            weekday.append(rate)
        else:
            weekend.append(rate)

    if not weekday or not weekend:
        return None

    if sum(weekday)/len(weekday) > sum(weekend)/len(weekend):
        return "📅 You tend to be more consistent on weekdays than weekends."
    else:
        return "📅 You tend to be more consistent on weekends than weekdays."


def generate_habit_stability_insight(habit_id, habit_name):
    logs = fetch_logs_for_habit(habit_id)
    if len(logs) < 7:
        return None

    values = [status for _, status in logs[-30:]]

    try:
        v = variance(values)
    except:
        return None

    if v < 0.1:
        return f"🧘 {habit_name} is very stable."
    elif v < 0.25:
        return f"⚖️ {habit_name} shows some inconsistency."
    else:
        return f"🌪️ {habit_name} is highly volatile."
