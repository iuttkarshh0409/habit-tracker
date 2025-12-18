from services.streaks import calculate_streak
from db.db_utils import fetch_completed_dates

def get_current_streak(habit_id):
    dates = fetch_completed_dates(habit_id)
    return calculate_streak(dates)
