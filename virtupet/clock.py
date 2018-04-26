# this file will have the functions to deal with the accumulation of time data and the printing of a timestamp

import time
import datetime


class Clock:

    def __init__(self):

        self.start = time.time()
        self.cur_time = 0

    def elapsed_time(self):
        return int(time.time() - self.start)

    def time_stamp(self):
        stamp = ""
        # hours = "%02d" % ((int((self.elapsed_time()))/ 60),)
        # minutes = "%02d" % (int((self.elapsed_time()))% 60,)
        # hours = "%02d" % ((int((time.time())) / 60),)
        # minutes = "%02d" % ((int((time.time())) % 60),)
        time = datetime.datetime.now()
        hours = "%02d" % (time.minute % 24,)
        minutes = "%02d" % (time.second,)

        if int(hours) == 00:
            return str(12) + ":" + minutes + "am"
        elif int(hours) == 13:
            return str(12) + ":" + minutes + "pm"
        else:
            return str(int(hours) % 12) + ":" + minutes + "pm"

    def update_time(self):
        self.cur_time = int(self.elapsed_time())

    def get_minutes(self):
        return "%02d" % (datetime.datetime.now().second, )

    def get_seconds(self):
        return "%02d" % (datetime.datetime.now().microsecond, )
