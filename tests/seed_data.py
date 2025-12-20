from datetime import date, timedelta
import random

from db.db_utils import insert_habit, log_habit_day, fetch_habits

# -----------------------
# Config
# -----------------------
HABITS = [
    "Read 20 pages",
    "Workout",
    "Meditate",
    "Drink 3L Water",
    "Journal",
    "Learn Python",
    "Sleep before 12",
    "No Junk Food",
    "Walk 8k steps",
    "Practice DSA"
]

DAYS_BACK = 30  # last 30 days

# -----------------------
# Insert habits
# -----------------------
for habit in HABITS:
    insert_habit(habit)

habits = fetch_habits()

# -----------------------
# Backfill logs
# -----------------------
for habit in habits:
    habit_id = habit[0]

    streak_bias = random.randint(0, 5)
    consistency = random.uniform(0.5, 0.9)

    for i in range(DAYS_BACK):
        log_date = date.today() - timedelta(days=i)

        # simulate streak breaks
        if i < streak_bias:
            status = 1
        else:
            status = 1 if random.random() < consistency else 0

        log_habit_day(habit_id, log_date, status)

print("Seed data inserted successfully.")
