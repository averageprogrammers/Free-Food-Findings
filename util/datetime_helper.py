import datetime
from dateutil import parser

def get_prev_and_next_sat(date_and_time):
    dt = parser.parse(dct["datetime"])
    weekday = (dt.weekday() + 2) % 7
    prev_saturday = (dt - datetime.timedelta(days=weekday)).date()
    next_saturday = (dt + datetime.timedelta(days=7-weekday)).date()
    return prev_saturday,next_saturday
