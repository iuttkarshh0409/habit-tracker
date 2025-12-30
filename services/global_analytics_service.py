from collections import defaultdict
from db.db_utils import fetch_all_logs_last_n_days, fetch_habits
from services.streak_service import get_current_streak
from services.consistency_service import get_consistency_percentage

def get_global_stats(days=30):
    habits = fetch_habits()

    total_habits = len(habits)
    if total_habits == 0:
        return None

    # Overall consistency
    logs = fetch_all_logs_last_n_days(days)
    completed = sum(1 for _, status in logs if status == 1)
    total = len(logs)
    overall_consistency = round((completed / total) * 100, 1) if total else 0.0

    # Per-habit stats
    consistency_map = {}
    streak_map = {}

    for habit_id, name, _, _ in habits:
        consistency_map[name] = get_consistency_percentage(habit_id, days)
        streak_map[name] = get_current_streak(habit_id)

    most_consistent = max(consistency_map, key=consistency_map.get)
    longest_streak = max(streak_map, key=streak_map.get)

    return {
        "total_habits": total_habits,
        "overall_consistency": overall_consistency,
        "most_consistent": most_consistent,
        "most_consistent_value": consistency_map[most_consistent],
        "longest_streak": longest_streak,
        "longest_streak_value": streak_map[longest_streak]
    }
