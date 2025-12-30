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
from services.global_analytics_service import get_global_stats
from services.export_service import export_logs_to_csv
from visualizations.charts import streak_timeline, weekly_completion


# ---------------- PAGE SETUP ----------------
st.title("Habit Tracker")

tab_overview, tab_analytics, tab_history = st.tabs(
    ["Overview", "Analytics", "History"]
)

habits = fetch_habits()


# ---------------- OVERVIEW TAB ----------------
with tab_overview:
    # Top row: Export button
    top_left, _ = st.columns([1, 5])

    with top_left:
        df_export = export_logs_to_csv()
        if df_export is not None:
            st.download_button(
                label="⬇️ Export Data",
                data=df_export.to_csv(index=False),
                file_name="habit_logs.csv",
                mime="text/csv",
                key="export_csv_btn"
            )

    # Global analytics
    stats = get_global_stats()
    if stats:
        st.subheader("📊 Overall Insights")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Habits", stats["total_habits"])
        col2.metric("Overall Consistency", f'{stats["overall_consistency"]}%')
        col3.metric(
            "Most Consistent",
            stats["most_consistent"],
            f'{stats["most_consistent_value"]}%'
        )
        col4.metric(
            "Longest Streak",
            stats["longest_streak"],
            f'{stats["longest_streak_value"]} days'
        )

        st.divider()

    # Add habit
    st.subheader("Add New Habit")

    habit_name = st.text_input("Habit name", key="add_habit_input")

    if st.button("Add Habit", key="add_habit_btn"):
        if habit_name.strip():
            insert_habit(habit_name.strip())
            st.success("Habit added")
            st.rerun()

    st.divider()

    # Sorting
    st.subheader("Your Habits")

    sort_option = st.selectbox(
        "Sort habits by",
        [
            "Streak (high → low)",
            "Consistency (high → low)",
            "Name (A → Z)"
        ],
        key="sort_habits_select"
    )

    if sort_option == "Streak (high → low)":
        habits = sorted(
            habits,
            key=lambda h: get_current_streak(h[0]),
            reverse=True
        )
    elif sort_option == "Consistency (high → low)":
        habits = sorted(
            habits,
            key=lambda h: get_consistency_percentage(h[0]),
            reverse=True
        )
    else:  # Name
        habits = sorted(habits, key=lambda h: h[1].lower())

    # Habit list
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
