import streamlit as st
from db.db_utils import insert_habit, fetch_habits
from services.streak_service import get_current_streak

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
