import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "habits.db"

def get_connection():
    return sqlite3.connect(DB_PATH)
from datetime import date
from .db_utils import get_connection

def insert_habit(name, frequency="daily"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habits (name, frequency, created_at)
        VALUES (?, ?, ?)
    """, (name, frequency, date.today()))

    conn.commit()
    conn.close()
from .db_utils import get_connection

def log_habit_day(habit_id, log_date, status):
    """
    status: 1 = completed, 0 = missed
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO logs (habit_id, date, status)
            VALUES (?, ?, ?)
        """, (habit_id, log_date, status))
        conn.commit()
    except sqlite3.IntegrityError:
        # log already exists for this habit & date
        pass
    finally:
        conn.close()

def fetch_habits():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, frequency, created_at
        FROM habits
        where is_active = 1
        ORDER BY created_at
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

from datetime import datetime

def fetch_completed_dates(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date
        FROM logs
        WHERE habit_id = ? AND status = 1
        ORDER BY date DESC
    """, (habit_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        datetime.strptime(row[0], "%Y-%m-%d").date()
        for row in rows
    ]

def fetch_logs_last_n_days(habit_id, days=30):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, status
        FROM logs
        WHERE habit_id = ?
        ORDER BY date DESC
        LIMIT ?
    """, (habit_id, days))

    rows = cursor.fetchall()
    conn.close()
    return rows

from datetime import date, timedelta

def fetch_completion_stats(habit_id, days=30):
    conn = get_connection()
    cursor = conn.cursor()

    start_date = date.today() - timedelta(days=days - 1)

    cursor.execute("""
        SELECT COUNT(*) 
        FROM logs
        WHERE habit_id = ?
          AND status = 1
          AND date >= ?
    """, (habit_id, start_date))

    completed_days = cursor.fetchone()[0]
    conn.close()

    return completed_days, days

def fetch_logs_for_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, status
        FROM logs
        WHERE habit_id = ?
        ORDER BY date DESC
    """, (habit_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

from datetime import date, timedelta

def fetch_all_logs_last_n_days(days=30):
    conn = get_connection()
    cursor = conn.cursor()

    start_date = date.today() - timedelta(days=days - 1)

    cursor.execute("""
        SELECT habit_id, status
        FROM logs
        WHERE date >= ?
    """, (start_date,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_all_logs_with_habits():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT h.name, l.date, l.status
        FROM logs l
        JOIN habits h ON l.habit_id = h.id
        ORDER BY l.date DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
def fetch_daily_completion_rate(days=30):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            l.date,
            SUM(l.status) as completed,
            COUNT(*) as total
        FROM logs l
        WHERE l.date >= DATE('now', ?)
        GROUP BY l.date
        ORDER BY l.date
    """, (f'-{days} days',))

    rows = cursor.fetchall()
    conn.close()
    return rows

def upsert_reflection_note(habit_id, date, note):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reflection_notes (habit_id, date, note)
        VALUES (?, ?, ?)
        ON CONFLICT(habit_id, date)
        DO UPDATE SET note = excluded.note
    """, (habit_id, date, note))

    conn.commit()
    conn.close()


def fetch_reflection_note(habit_id, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT note
        FROM reflection_notes
        WHERE habit_id = ? AND date = ?
    """, (habit_id, date))

    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def fetch_reflection_notes_in_range(habit_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, note
        FROM reflection_notes
        WHERE habit_id = ?
          AND date BETWEEN ? AND ?
    """, (habit_id, start_date, end_date))

    rows = cursor.fetchall()
    conn.close()
    return rows

def archive_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE habits
        SET is_active = 0
        WHERE id = ?
    """, (habit_id,))

    conn.commit()
    conn.close()

def fetch_archived_habits():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, frequency, created_at
        FROM habits
        WHERE is_active = 0
        ORDER BY created_at ASC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def restore_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE habits
        SET is_active = 1
        WHERE id = ?
    """, (habit_id,))

    conn.commit()
    conn.close()

