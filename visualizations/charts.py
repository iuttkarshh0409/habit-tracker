import plotly.express as px
import pandas as pd
from datetime import datetime

def streak_timeline(logs):
    """
    logs: [(date, status), ...]
    """
    if not logs:
        return None

    df = pd.DataFrame(logs, columns=["date", "status"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    return px.line(
        df,
        x="date",
        y="status",
        markers=True,
        title="Habit Completion Timeline",
        labels={"status": "Completed (1 = Yes)"}
    )
def weekly_completion(logs):
    if not logs:
        return None

    df = pd.DataFrame(logs, columns=["date", "status"])
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.strftime("%Y-%U")

    weekly = df.groupby("week")["status"].sum().reset_index()

    return px.bar(
        weekly,
        x="week",
        y="status",
        title="Weekly Habit Completion",
        labels={"status": "Days Completed"}
    )


def global_completion_trend(rows):
    if not rows:
        return None

    df = pd.DataFrame(
        rows,
        columns=["date", "completed", "total"]
    )

    df["date"] = pd.to_datetime(df["date"])
    df["completion_rate"] = (df["completed"] / df["total"]) * 100

    return px.line(
        df,
        x="date",
        y="completion_rate",
        markers=True,
        title="Overall Habit Completion Trend",
        labels={"completion_rate": "Completion %"},
        range_y=[0, 100]
    )
