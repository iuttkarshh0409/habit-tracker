# Habit Tracker & Personal Analytics Dashboard

A data-driven habit tracking application built in Python that helps users track daily habits, analyze long-term consistency, and understand behavioral patterns through explainable analytics and contextual insights.

This project prioritizes **data transparency**, **clean architecture**, and **interpretability** over gamification, notifications, or streak pressure.

---

## 📌 Overview

Most habit-tracking apps optimize for streaks, motivation hacks, or paywalled insights.  
This project takes a different approach:

**Habits are treated as data, not as moral judgments.**

The application focuses on:
- Honest measurement over encouragement  
- Long-term patterns over short-term streaks  
- Context over guilt  

It is designed as a practical Python project demonstrating modular architecture, persistent storage, analytics, and responsible interpretation of user data.

---

## ✨ Core Features

### Habit Management
- Create and manage multiple daily habits  
- Persistent storage using a relational SQLite database  

### Daily Check-In System
- Log each habit as **Completed** or **Missed**  
- One entry per habit per day enforced at the database level  

### Automated Streak Calculation
- Current streaks computed dynamically from log history  
- No stored or duplicated streak values, ensuring data integrity  

### Consistency Analytics
- 7-day and 30-day consistency views  
- Separates short-term momentum from long-term behavior  
- Avoids over-reliance on streaks alone  

### Interactive Analytics Dashboard
- Global completion trends across all habits  
- Per-habit analytics with expandable sections  
- Built using interactive Plotly visualizations  

### Insight Engine (Explainable & Conservative)
- Insights generated only when statistically meaningful  
- Confidence thresholds to avoid noise and overfitting  
- No insights shown when data is insufficient  
- Clear *“Why am I seeing this?”* explanations for transparency  

### Reflection Notes (Context Without Judgment)
- Optional habit-per-day reflection notes  
- Lightweight context such as *“Travel day”* or *“Exam week”*  
- Notes never affect streaks or consistency calculations  
- Used only for contextual interpretation  

### Insight Attribution Using Notes
- Insights may reference reflection notes when patterns align  
- Uses correlation language (“coincided with”), not causation  
- Gracefully suppressed when attribution is inconclusive  

### History View
- Transparent chronological view of all habit logs  
- Reflection notes displayed alongside entries  
- Raw data always accessible  

### Data Export
- Global CSV export of all habit logs  
- Per-habit CSV export  

---

## 🛠 Tech Stack

- **Language:** Python 3.10+  
- **UI Framework:** Streamlit  
- **Database:** SQLite  
- **Visualization:** Plotly  
- **Architecture:** Modular, service-oriented design  
- **Deployment (Optional):** Streamlit Community Cloud  

---

## 🏗 Project Architecture

The project follows **Separation of Concerns**, keeping UI, business logic, database access, analytics, and interpretation clearly isolated.

```
habit-tracker/
│
├── app.py
├── requirements.txt
├── README.md
│
├── db/
│   ├── db_utils.py
│   └── habits.db
│
├── services/
│   ├── checkin_service.py
│   ├── streak_service.py
│   ├── consistency_service.py
│   ├── global_analytics_service.py
│   ├── export_service.py
│   ├── insight_service.py
│   └── reflection_service.py
│
├── visualizations/
│   └── charts.py
│
├── models/
│   └── __init__.py
│
└── tests/
    └── seed_data.py
```

---

## 📊 Analytics Explained

### Streak
- Measures consecutive completed days up to today  
- Automatically resets when a day is missed  

### Consistency Percentage
- Completion rate over a selected window (7 or 30 days)

**Formula**
```
(Completed Days ÷ Total Days) × 100
```

This provides a more realistic view of behavior than streaks alone.

### Insights
- Generated only when sufficient data exists  
- Suppressed when patterns are weak or inconclusive  
- Always accompanied by transparent explanations  

---

## ▶️ Running the Project Locally

Clone the repository:
```
git clone <repo-url>
cd habit-tracker
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the application:
```
streamlit run app.py
```

---

## 🧪 Sample Data (Optional)

For development and visualization testing:
```
python -m tests.seed_data
```

Populates the database with realistic historical logs.  
**Intended for local testing only.**

---

## 🔖 Versioning

**Current Version:** v0.4.0

### v0.4.0 Includes
- Reflection notes (habit-per-day)  
- Insight attribution using contextual notes  
- Confidence thresholds for all insights  
- Weekly / monthly analytics toggle  
- Explainable analytics with transparent UX  
- Global and per-habit CSV export  

Earlier versions focused on:
- Tracking (v0.1)  
- Analytics (v0.2)  
- Interpretation (v0.3)  

---

## 🎯 What This Project Demonstrates

- Clean, modular Python application design  
- Relational data modeling with SQLite  
- Responsible analytics and interpretation  
- UI design that favors clarity over gamification  
- Feature discipline and intentional versioning  
