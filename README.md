# Habit Tracker & Personal Analytics Dashboard

A data-driven habit tracking application built in Python that empowers users to monitor daily routines, analyze consistency, and visualize progress through automated analytics.

---

## 📌 Overview
This project is a personal, open-source alternative to subscription-based habit trackers. Unlike apps that hide user data behind paywalls, this dashboard focuses on **data transparency** and **behavioral insight**. The core emphasis is on state management, persistent storage, and modular software architecture.

### Key Features
* **Habit Management:** Create and manage custom daily habits.
* **Dynamic Log System:** Record completions with a per-day status (Completed/Missed).
* **Automated Streak Logic:** Dynamic calculation of current and all-time high streaks without data redundancy.
* **Interactive Analytics:** Real-time visualizations using Plotly and Seaborn.
* **Relational Persistence:** Robust local storage using a structured SQLite database.

---

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Framework:** Streamlit (App UI & State)
* **Database:** SQLite (Relational Storage)
* **Visualization:** Plotly, Matplotlib, Seaborn
* **Deployment:** Streamlit Cloud

---

## 🏗 Project Architecture
The codebase follows the **Separation of Concerns** principle, making it modular and easy to extend.

```text
habit-tracker/
│
├── app.py                # Streamlit application entry point
├── db/
│   └── habits.db         # SQLite relational database
├── models/
│   ├── habit.py          # Habit data structures
│   └── log.py            # Daily habit logs & schemas
├── services/
│   └── streaks.py        # Core logic for streak & consistency calculation
├── visualizations/
│   └── charts.py         # Plotly & Seaborn chart generators
├── requirements.txt      # Project dependencies
└── README.md