import datetime
import time

def get_seconds_time_from_ingame_timestamp(ingame_time):
    return int(ingame_time/1000)

def get_date_string_from_file_name(file_name):
    # The typical name for a game file looks something like this
    # MP Replay v101.101.39515.0 @2020.08.23 145114 (2).aoe2record
    return file_name.split('@')[1].split()[0]

def get_timestamp_for_date_string(date_string):
    # 43200 is 12 hours -> we guess the game started at noon since we don't know the exact time
    return int(time.mktime(datetime.datetime.strptime(date_string, "%Y.%m.%d").timetuple()) + 43200)