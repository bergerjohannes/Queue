import datetime

def get_readable_time_from_ingame_timestamp(ingame_time):
    return str(datetime.timedelta(milliseconds=ingame_time))