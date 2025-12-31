# Data Schema – Habit Tracker Export

This document defines the canonical data schema used for exporting habit data
for analysis and research purposes.

Once users begin contributing data, this schema is considered stable and
backward-compatible.

---

## Export File

**File name:** `habit_logs_export.csv`  
**Granularity:** One row per habit per calendar date  
**Date format:** ISO 8601 (`YYYY-MM-DD`)

---

## Columns

### `user_id`
- Integer
- Identifies the user who owns the habit
- Currently fixed at `1` for single-user mode
- Reserved for future multi-user support

---

### `habit_id`
- Integer
- Unique identifier for a habit
- Stable across exports

---

### `habit_name`
- String
- Human-readable habit label
- Not guaranteed to be unique

---

### `date`
- Date
- Calendar date of the habit log
- No timezone component

---

### `status`
- Integer (binary)
- `1` = Completed
- `0` = Missed

---

### `is_active`
- Integer (binary)
- Indicates whether the habit was active at the time of export
- `1` = Active
- `0` = Archived

---

### `consistency_7d`
- Float (percentage)
- Completion rate over the 7 days ending on `date`
- Calculated as:  
  `(sum(status) / number of logged days) × 100`

---

### `consistency_30d`
- Float (percentage)
- Completion rate over the 30 days ending on `date`

---

### `streak_on_date`
- Integer
- Length of the active completion streak up to and including `date`
- Resets after a missed day

---

### `has_reflection`
- Integer (binary)
- Indicates whether a reflection note exists for this habit on this date
- `1` = Reflection present
- `0` = No reflection

---

## Notes on Ethics & Privacy

- Reflection text is intentionally excluded from exports
- No personally identifiable information is collected
- All analytics are derived from user-consented data

---

## Intended Use

This schema is designed for:
- longitudinal behavioral analysis
- statistical modeling
- case studies or minor research publications
- reproducible analysis in Python, R, or SQL

The schema prioritizes clarity, stability, and interpretability over convenience.
