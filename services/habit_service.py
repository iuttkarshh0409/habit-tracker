from db.db_utils import archive_habit

def archive(habit_id):
    archive_habit(habit_id)

from db.db_utils import restore_habit

def restore(habit_id):
    restore_habit(habit_id)
