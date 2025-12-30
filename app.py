import streamlit as st
import pandas as pd

from db.db_utils import (
    insert_habit,
    fetch_habits,
    fetch_logs_last_n_days,
    fetch_logs_for_habit,
    fetch_daily_completion_rate
)
from services.streak_service import get_current_streak
from services.checkin_service import check_in_today
from services.consistency_service import get_consistency_percentage
from services.global_analytics_service import get_global_stats
from services.export_service import (
    export_logs_to_csv,
    export_habit_logs_to_csv
)
from visualizations.charts import (
    streak_timeline,
    weekly_completion,
    global_completion_trend
)
from services.insight_service import (
    generate_global_trend_insight,
    generate_weekday_weekend_insight,
    generate_habit_stability_insight
)


# ---------------- PAGE SETUP ----------------
st.title("Habit Tracker")

tab_overview, tab_analytics, tab_history = st.tabs(
    ["Overview", "Analytics", "History"]
)

habits = fetch_habits()

# ================= OVERVIEW TAB =================
with tab_overview:
    # Export (top-left)
    top_left, _ = st.columns([1, 5])
    with top_left:
        df_export = export_logs_to_csv()
        if df_export is not None:
            st.download_button(
                "⬇️ Export Data",
                df_export.to_csv(index=False),
                "habit_logs.csv",
                "text/csv",
                key="export_csv_btn"
            )

    # Global stats (always 30 days)
    stats = get_global_stats()
    if stats:
        st.subheader("📊 Overall Insights")
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Habits", stats["total_habits"])
        c2.metric("Overall Consistency", f'{stats["overall_consistency"]}%')
        c3.metric(
            "Most Consistent",
            stats["most_consistent"],
            f'{stats["most_consistent_value"]}%'
        )
        c4.metric(
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

    # Sorting (Overview = 30-day logic)
    st.subheader("Your Habits")
    sort_option = st.selectbox(
        "Sort habits by",
        ["Streak (high → low)", "Consistency (high → low)", "Name (A → Z)"],
        key="sort_habits_select"
    )

    if sort_option == "Streak (high → low)":
        habits = sorted(habits, key=lambda h: get_current_streak(h[0]), reverse=True)
    elif sort_option == "Consistency (high → low)":
        habits = sorted(
            habits,
            key=lambda h: get_consistency_percentage(h[0], days=30),
            reverse=True
        )
    else:
        habits = sorted(habits, key=lambda h: h[1].lower())

    # Habit rows
    for habit_id, name, _, _ in habits:
        streak = get_current_streak(habit_id)
        consistency = get_consistency_percentage(habit_id, days=30)

        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

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

        with col4:
            df_habit = export_habit_logs_to_csv(habit_id)
            if df_habit is not None:
                st.download_button(
                    "📄",
                    df_habit.to_csv(index=False),
                    f"{name.replace(' ', '_').lower()}_history.csv",
                    "text/csv",
                    key=f"export_habit_{habit_id}"
                )

# ================= ANALYTICS TAB =================
with tab_analytics:
    time_window = st.radio(
        "View range",
        ["Last 7 days", "Last 30 days"],
        horizontal=True,
        key="time_window_toggle"
    )

    days = 7 if time_window == "Last 7 days" else 30
    st.caption("Weekly view shows momentum. Monthly view shows stability.")

    st.subheader("📈 Global Trend")
    rows = fetch_daily_completion_rate(days=days)
    trend_fig = global_completion_trend(rows)

    if trend_fig:
        st.plotly_chart(
            trend_fig,
            width="stretch",
            key="global_trend_chart"
        )

    st.divider()
    st.subheader("🧠 Insights")

    trend_insight = generate_global_trend_insight()
    weekday_insight = generate_weekday_weekend_insight()

    if trend_insight:
        st.write(trend_insight)

    if weekday_insight:
        st.write(weekday_insight)

    st.divider()
    st.subheader("Habit Analytics")

    if not habits:
        st.info("Add habits to see analytics")
    else:
        for habit_id, name, _, _ in habits:
            with st.expander(name):
                habit_insight = generate_habit_stability_insight(habit_id, name)
                if habit_insight:
                    st.caption(habit_insight)

                logs = fetch_logs_last_n_days(habit_id, days=days)

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
                  

# ================= HISTORY TAB =================
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
                df["Status"] = df["Status"].map({1: "Completed", 0: "Missed"})
                st.dataframe(df, use_container_width=True)
            else:
                st.caption("No logs yet")

            st.divider()
