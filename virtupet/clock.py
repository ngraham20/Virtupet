# this file will have the functions to deal with the accumulation of time data and the printing of a timestamp

import time


class Clock:

    def __init__(self):

        self.start = time.time()
        self.cur_time = 0

    def elapsed_time(self):
        return int(time.time() - self.start)

    def time_stamp(self):
        stamp = ""
        hours = "%02d" % ((int((self.elapsed_time()))/60),)
        minutes = "%02d" % (int((self.elapsed_time())),)

        return hours + ":" + minutes

    def update_time(self):
        self.cur_time = int(self.elapsed_time())
