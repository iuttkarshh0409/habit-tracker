import requests
from datetime import datetime

SCRIPT_URL="https://script.google.com/macros/s/AKfycbxpGSx9AMYIkf3t_41jA_YPHXVT7kMMjQH9KB9IMApVfdGXdSYjOXRKtRbUAxSMeDG2/exec"

def send_to_sheet(row):
    payload = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "user_id": row["user_id"],
        "habit_id": row["habit_id"],
        "habit_name": row["habit_name"],
        "date": row["date"],
        "status": row["status"],
        "is_active": row["is_active"],
        "consistency_7d": row["consistency_7d"],
        "consistency_30d": row["consistency_30d"],
        "streak_on_date": row["streak_on_date"],
        "has_reflection": row["has_reflection"],
        "schema_version": "1.0"
    }

    requests.post(SCRIPT_URL, json=payload, timeout=10)
