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