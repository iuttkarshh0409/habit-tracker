#--------------- IMPORTS -----------------
import streamlit as st
import pandas as pd

from db.db_utils import (
    insert_habit,
    fetch_habits,
    fetch_logs_last_n_days,
    fetch_logs_for_habit,
    fetch_daily_completion_rate
)

from services.habit_service import archive
from db.db_utils import fetch_archived_habits
from services.habit_service import restore
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
    generate_insight_attribution,
    generate_weekday_weekend_insight,
    generate_habit_stability_insight
)

from services.reflection_service import (
    save_reflection,
    get_reflection
)

# ---------------- PAGE SETUP ----------------
st.title("Habit Tracker")

tab_overview, tab_analytics, tab_history = st.tabs(
    ["Overview", "Analytics", "History"]
)

habits = fetch_habits()

# ================= OVERVIEW TAB =================
with tab_overview:
    # Export 
    top_left, _ = st.columns([1, 5])
    with top_left:
        df_export = export_logs_to_csv()
        if df_export is not None:
            st.download_button(
                "⬇️ Export Data",
                df_export.to_csv(index=False),
                "habit_logs.csv",
                "text/csv",
                key="export_csv_btn",
                help="Export all your habit logs as a CSV file."
            )

    # Global stats
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

    # Sorting 
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

        col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])

        with col1:
            st.write(
                f"🔥 **{name}** — {streak} day streak · "
                f"**{consistency}% consistency**"
            )

        with col2:
            if st.button("✅", key=f"done_{habit_id}", help="Mark as done for today"):
                check_in_today(habit_id, True)
                st.rerun()

        with col3:
            if st.button("❌", key=f"miss_{habit_id}", help="Mark as missed for today"):
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
                    key=f"export_habit_{habit_id}",
                    help="Export this habit's logs as a CSV file."
                )

        with col5:
            if st.button("🗄️", key=f"archive_{habit_id}", help="Archive this habit"):
                archive(habit_id)
                st.success(f"Habit '{name}' archived")
                st.rerun()


    st.divider()

archived = fetch_archived_habits()

if archived:
    with st.expander("🗄️ Archived Habits"):
        st.caption("Archived habits are read-only. You can restore them anytime.")

        for habit_id, name, _, _ in archived:
            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(f"**{name}**")

            with col2:
                if st.button("↩️ Restore", key=f"restore_{habit_id}"):
                    restore(habit_id)
                    st.success("Habit restored")
                    st.rerun()


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

    st.subheader(
        "🧠 Insights",
        help=(
            "Insights are generated only when enough data is available. "
            "They are based on statistically meaningful patterns, not single-day changes."
        )
    )

    trend_insight = generate_global_trend_insight()
    weekday_insight = generate_weekday_weekend_insight()

    if trend_insight:
        st.write(trend_insight)

    if weekday_insight:
        st.write(weekday_insight)

    st.divider()

    with st.expander("Why am I seeing these insights?"):
        st.markdown("""
**How insights are generated:**

- **Trend insight**  
  Compares average completion rates across two time periods.  
  Shown only if the change is large enough to be meaningful.

- **Weekday vs Weekend**  
  Compares consistency on weekdays and weekends.  
  Requires sufficient data from both categories.

- **Habit stability**  
  Measures how consistently a habit is completed over time.  
  Stable habits vary less day-to-day; volatile ones vary more.

If there isn’t enough reliable data, no insight is shown.
""")

    st.subheader("Habit Analytics")

    if not habits:
        st.info("Add habits to see analytics")
    else:
        for habit_id, name, _, _ in habits:
            with st.expander(name):
                habit_insight = generate_habit_stability_insight(habit_id, name)

                if habit_insight:
                    st.caption(
                        habit_insight,
                        help=(
                            "Habit stability is based on how often this habit is completed "
                            "over time. More variation means lower stability."
                        )
                    )

                    attribution = generate_insight_attribution(
                        habit_id,
                        days=days
                    )

                    if attribution:
                        st.caption(
                            f"ℹ️ {attribution}",
                            help=(
                                "Add short reflection notes in the History tab to help "
                                "connect patterns with real-life context."
                            )
                        )

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
                for date, status in logs:
                    status_text = "Completed" if status == 1 else "Missed"
                    st.write(f"**{date}** — {status_text}")

                    existing_note = get_reflection(habit_id, date)

                    with st.expander("📝 Add context", expanded=False):
                        note = st.text_area(
                            "Reflection (optional)",
                            value=existing_note or "",
                            max_chars=120,
                            placeholder="Add context (optional)",
                            key=f"note_{habit_id}_{date}"
                        )

                        if st.button(
                            "Save note",
                            key=f"save_note_{habit_id}_{date}"
                        ):
                            save_reflection(habit_id, date, note)
                            st.success("Note saved")
                            st.rerun()

                st.divider()
            else:
                st.caption("No logs yet")
                st.divider()
