from db.db_utils import (
    upsert_reflection_note,
    fetch_reflection_note
)

def save_reflection(habit_id, date, note):
    if not note.strip():
        return
    upsert_reflection_note(habit_id, date, note.strip())


def get_reflection(habit_id, date):
    return fetch_reflection_note(habit_id, date)
