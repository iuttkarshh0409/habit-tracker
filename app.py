import streamlit as st
from db.db_utils import fetch_logs_last_n_days
from visualizations.charts import streak_timeline, weekly_completion

from db.db_utils import insert_habit, fetch_habits
from services.streak_service import get_current_streak

from services.consistency_service import get_consistency_percentage


st.title("Habit Tracker")

st.subheader("Add New Habit")
habit_name = st.text_input("Habit name")

if st.button("Add Habit"):
    if habit_name:
        insert_habit(habit_name)
        st.success("Habit added")

st.divider()
st.subheader("Your Habits")

habits = fetch_habits()

for h in habits:
    habit_id, name, _, _ = h
    streak = get_current_streak(habit_id)
    st.write(f"🔥 {name} — {streak} day streak")

    logs = fetch_logs_last_n_days(habit_id)

    timeline_fig = streak_timeline(logs)
    weekly_fig = weekly_completion(logs)

    if timeline_fig:
       st.plotly_chart(timeline_fig, use_container_width=True)

    if weekly_fig:
       st.plotly_chart(weekly_fig, use_container_width=True)

    consistency = get_consistency_percentage(habit_id)

    st.write(
       f"🔥 **{name}** — {streak} day streak · "
       f"**{consistency}% consistency (30 days)**"
    )

