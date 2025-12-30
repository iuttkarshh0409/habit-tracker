from datetime import date
from db.db_utils import (
    insert_habit,
    log_habit_day,
    fetch_habits,
    fetch_completed_dates
)

# Insert a habit
insert_habit("Read 20 pages")

# Fetch habits
habits = fetch_habits()
print("Habits:", habits)

# Pick first habit
habit_id = habits[0][0]

# Log some days
log_habit_day(habit_id, date.today(), 1)
log_habit_day(habit_id, date.today(), 1)  # duplicate test for edge case testing
log_habit_day(habit_id, date.today(), 0)

# Fetch completed dates
completed = fetch_completed_dates(habit_id)
print("Completed dates:", completed)
