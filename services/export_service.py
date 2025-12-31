import pandas as pd
from db.db_utils import get_connection

def export_logs_to_csv():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                SELECT
    1 AS user_id,
    h.id AS habit_id,
    h.name AS habit_name,
    l.date AS date,
    l.status AS status,
    h.is_active AS is_active,

    -- Consistency snapshots
    (
        SELECT ROUND(AVG(l2.status) * 100, 1)
        FROM habit_logs l2
        WHERE l2.habit_id = h.id
          AND l2.date BETWEEN DATE(l.date, '-6 days') AND l.date
    ) AS consistency_7d,

    (
        SELECT ROUND(AVG(l3.status) * 100, 1)
        FROM habit_logs l3
        WHERE l3.habit_id = h.id
          AND l3.date BETWEEN DATE(l.date, '-29 days') AND l.date
    ) AS consistency_30d,

    -- Streak up to that date
    (
        SELECT COUNT(*)
        FROM habit_logs s
        WHERE s.habit_id = h.id
          AND s.status = 1
          AND s.date <= l.date
          AND s.date >= (
              SELECT COALESCE(
                  MAX(m.date),
                  '1970-01-01'
              )
              FROM habit_logs m
              WHERE m.habit_id = h.id
                AND m.status = 0
                AND m.date < l.date
          )
    ) AS streak_on_date,

    -- Reflection presence
    CASE
        WHEN r.note IS NOT NULL THEN 1
        ELSE 0
    END AS has_reflection

FROM habit_logs l
JOIN habits h ON h.id = l.habit_id
LEFT JOIN reflection_notes r
    ON r.habit_id = l.habit_id
   AND r.date = l.date

ORDER BY h.id, l.date;

    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    df = pd.DataFrame(
        rows,
        columns=[
            "user_id",
            "habit_id",
            "habit_name",
            "date",
            "status",
            "is_active",
            "consistency_7d",
            "consistency_30d",
            "streak_on_date",
            "has_reflection"
        ]
    )

    # Enforce types (critical for research)
    df["date"] = pd.to_datetime(df["date"])
    df["status"] = df["status"].astype(int)
    df["is_active"] = df["is_active"].astype(int)
    df["has_reflection"] = df["has_reflection"].astype(int)

    return df
