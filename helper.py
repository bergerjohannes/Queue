import datetime
import time

def get_readable_time_from_ingame_timestamp(ingame_time):
    return str(datetime.timedelta(milliseconds=ingame_time)).split('.')[0]

def get_timestamp_for_date_string(date_string):
    # 43200 is 12 hours -> we guess the game started at noon since we don't know the exact time
    return int(time.mktime(datetime.datetime.strptime(date_string, "%Y.%m.%d").timetuple()) + 43200)