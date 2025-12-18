from datetime import datetime, timedelta

def calculate_streak(log_dates):
    """
    log_dates: list of dates where habit was completed
    returns: current streak count
    """
    if not log_dates:
        return 0

    log_dates = sorted(log_dates, reverse=True)
    streak = 0
    today = datetime.today().date()

    expected_date = today

    for d in log_dates:
        if d == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        elif d < expected_date:
            break

    return streak
