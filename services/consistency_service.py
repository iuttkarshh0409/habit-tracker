from db.db_utils import fetch_completion_stats

def get_consistency_percentage(habit_id, days=30):
    completed, total = fetch_completion_stats(habit_id, days)
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 1)

