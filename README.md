# Habit Tracker & Personal Analytics Dashboard

A data-driven habit tracking application built in Python that allows users to track daily habits, analyze consistency, and visualize behavioral trends through an interactive dashboard.

This project emphasizes **data transparency**, **clean architecture**, and **meaningful analytics** rather than gamification or paywalled insights.

---

## 📌 Overview

Most habit-tracking apps focus on streak pressure while hiding user data behind subscriptions.  
This project takes a different approach: it treats habits as data, not guilt machines.

The application enables users to:
- Log daily habit outcomes  
- Compute streaks dynamically  
- Measure long-term consistency  
- Explore progress through interactive visualizations  

The goal is to demonstrate practical Python application development using persistent storage, modular services, and data visualization.

---

## ✨ Core Features

### Habit Management
- Create and manage multiple daily habits  
- Persistent storage using a relational database  

### Daily Check-In System
- Log each habit as **Completed** or **Missed** per day  
- Duplicate entries per day prevented at the database level  

### Automated Streak Calculation
- Current streaks computed dynamically from log history  
- No redundant or stored streak values, ensuring data integrity  

### Consistency Analytics
- 30-day consistency percentage per habit  
- Separates short-term streaks from long-term behavior patterns  

### Interactive Analytics Dashboard
- Timeline view of habit completion  
- Weekly completion summaries  
- Built using interactive Plotly charts  

### History View
- Transparent, tabular view of all habit logs  
- Raw data always accessible to the user  

---

## 🛠 Tech Stack

- **Language:** Python 3.10+  
- **UI Framework:** Streamlit  
- **Database:** SQLite  
- **Visualization:** Plotly (primary), Matplotlib & Seaborn (supporting)  
- **Architecture:** Modular service-based design  
- **Deployment (Optional):** Streamlit Cloud  

---

## 🏗 Project Architecture

The project follows **Separation of Concerns**, keeping UI, business logic, database access, and visualization isolated.

```
habit-tracker/
│
├── app.py                     # Streamlit application entry point
├── requirements.txt           # Project dependencies
├── README.md
│
├── db/
│   ├── __init__.py
│   ├── db_utils.py            # Database helpers & queries
│   └── habits.db              # SQLite database (sample/demo data)
│
├── services/
│   ├── __init__.py
│   ├── checkin_service.py     # Daily habit check-in logic
│   ├── streaks.py             # Core streak calculation logic
│   ├── streak_service.py      # DB → streak integration
│   └── consistency_service.py # Consistency percentage logic
│
├── visualizations/
│   ├── __init__.py
│   └── charts.py              # Plotly chart generators
│
├── models/
│   └── __init__.py            # Reserved for future domain models
│
└── tests/
    ├── __init__.py
    └── seed_data.py           # Development-only seed data script
```

---

## 📊 Analytics Explained

### Streak
- Measures consecutive completed days up to today  
- Resets automatically when a day is missed  

### Consistency Percentage
- Measures habit completion over the last 30 days  

**Formula**
```
(Completed Days ÷ Total Days) × 100
```

Provides a more realistic picture of long-term behavior.

This dual-metric approach avoids over-reliance on streaks alone.

---

## ▶️ Running the Project Locally

1. Clone the repository
```
git clone <repo-url>
cd habit-tracker
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Run the app
```
streamlit run app.py
```

---

## 🧪 Sample Data (Optional)

For development and visualization testing, a seed script is included:
```
python -m tests.seed_data
```

This populates the database with multiple habits and realistic historical logs.  
**Note:** Intended for local testing only.

---

## 🔖 Versioning

**Current Version:** v0.1.0

Includes:
- Core habit tracking  
- Persistent storage  
- Streak and consistency metrics  
- Tab-based UI (Overview | Analytics | History)  
- Interactive data visualizations  

---

## 🚧 Planned Improvements

- Global analytics across all habits  
- Export logs and analytics as CSV  
- Habit sorting and filtering  
- Authentication & multi-user support  
- Cloud database integration  
- Advanced trend detection  

---

## 🎯 What This Project Demonstrates

- Practical Python application development  
- Clean modular architecture  
- Real-world state and persistence handling  
- Data-driven feature design  
- Visualization as insight, not decoration  
