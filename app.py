import streamlit as st
import pandas as pd

from db.db_utils import (
    insert_habit,
    fetch_habits,
    fetch_logs_last_n_days,
    fetch_logs_for_habit
)
from services.streak_service import get_current_streak
from services.checkin_service import check_in_today
from services.consistency_service import get_consistency_percentage
from visualizations.charts import streak_timeline, weekly_completion

st.title("Habit Tracker")

tab_overview, tab_analytics, tab_history = st.tabs(
    ["Overview", "Analytics", "History"]
)

habits = fetch_habits()

# ---------------- OVERVIEW TAB ----------------
with tab_overview:
    st.subheader("Add New Habit")

    habit_name = st.text_input("Habit name", key="add_habit_input")

    if st.button("Add Habit", key="add_habit_btn"):
        if habit_name.strip():
            insert_habit(habit_name.strip())
            st.success("Habit added")
            st.rerun()

    st.divider()
    st.subheader("Your Habits")

    for habit_id, name, _, _ in habits:
        streak = get_current_streak(habit_id)
        consistency = get_consistency_percentage(habit_id)

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            st.write(
                f"🔥 **{name}** — {streak} day streak · "
                f"**{consistency}% consistency**"
            )

        with col2:
            if st.button("✅", key=f"done_{habit_id}"):
                check_in_today(habit_id, True)
                st.rerun()

        with col3:
            if st.button("❌", key=f"miss_{habit_id}"):
                check_in_today(habit_id, False)
                st.rerun()

# ---------------- ANALYTICS TAB ----------------
with tab_analytics:
    st.subheader("Habit Analytics")

    if not habits:
        st.info("Add habits to see analytics")
    else:
        for habit_id, name, _, _ in habits:
            st.markdown(f"### {name}")

            logs = fetch_logs_last_n_days(habit_id)

            timeline_fig = streak_timeline(logs)
            weekly_fig = weekly_completion(logs)

            if timeline_fig:
                st.plotly_chart(
                    timeline_fig,
                    width="stretch",
                    key=f"timeline_{habit_id}"
                )

            if weekly_fig:
                st.plotly_chart(
                    weekly_fig,
                    width="stretch",
                    key=f"weekly_{habit_id}"
                )

            st.divider()

# ---------------- HISTORY TAB ----------------
with tab_history:
    st.subheader("Habit History")

    if not habits:
        st.info("No history yet")
    else:
        for habit_id, name, _, _ in habits:
            st.markdown(f"### {name}")

            logs = fetch_logs_for_habit(habit_id)

            if logs:
                df = pd.DataFrame(logs, columns=["Date", "Status"])
                df["Status"] = df["Status"].map(
                    {1: "Completed", 0: "Missed"}
                )
                st.dataframe(df, use_container_width=True)
            else:
                st.caption("No logs yet")

            st.divider()
