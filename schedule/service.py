from datetime import datetime, timedelta
from .config import AGENDA_CONFIG

# Standby
def generate_daily_slots(date):
    slots = []

    current = datetime.combine(date, AGENDA_CONFIG["START_TIME"])
    end = datetime.combine(date, AGENDA_CONFIG["END_TIME"])

    while current < end:
        slots.append(current)
        current += timedelta(minutes=AGENDA_CONFIG["SLOT_MINUTES"])

    return slots


from datetime import datetime, timedelta, date
from .config import AGENDA_CONFIG


def generate_time_choices():
    current = datetime.combine(date.today(), AGENDA_CONFIG["START_TIME"])
    end = datetime.combine(date.today(), AGENDA_CONFIG["END_TIME"])

    choices = []
    while current < end:
        hour_str = current.strftime("%H:%M")
        choices.append((hour_str, hour_str))
        current += timedelta(minutes=AGENDA_CONFIG["SLOT_MINUTES"])

    return choices