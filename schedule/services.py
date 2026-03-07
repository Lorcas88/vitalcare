from datetime import datetime, timedelta
from .config import AGENDA_CONFIG


def generate_daily_slots(date):
    slots = []

    current = datetime.combine(date, AGENDA_CONFIG["START_TIME"])
    end = datetime.combine(date, AGENDA_CONFIG["END_TIME"])

    while current < end:
        slots.append(current)
        current += timedelta(minutes=AGENDA_CONFIG["SLOT_MINUTES"])

    return slots