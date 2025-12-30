import pandas as pd
from db.db_utils import fetch_all_logs_with_habits

def export_logs_to_csv():
    logs = fetch_all_logs_with_habits()

    if not logs:
        return None

    df = pd.DataFrame(
        logs,
        columns=["Habit", "Date", "Status"]
    )

    df["Status"] = df["Status"].map(
        {1: "Completed", 0: "Missed"}
    )

    return df
