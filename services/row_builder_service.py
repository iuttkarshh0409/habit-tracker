from services.consistency_service import get_consistency_percentage
from services.streak_service import get_current_streak
from services.reflection_service import get_reflection

def build_row(habit_id, habit_name, status, date):
    return {
        "user_id": 1,  # single-user for now
        "habit_id": habit_id,
        "habit_name": habit_name,
        "date": date,
        "status": status,
        "is_active": 1,
        "consistency_7d": get_consistency_percentage(habit_id, days=7),
        "consistency_30d": get_consistency_percentage(habit_id, days=30),
        "streak_on_date": get_current_streak(habit_id),
        "has_reflection": 0  # reflection may come later
    }
