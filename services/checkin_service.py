from datetime import date
from db.db_utils import log_habit_day

def check_in_today(habit_id, completed: bool):
    """
    Logs today's status for a habit.
    completed = True  -> status 1
    completed = False -> status 0
    """
    status = 1 if completed else 0
    log_habit_day(habit_id, date.today(), status)
