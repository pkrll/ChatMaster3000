import urwid, time
from twisted.internet import task
from collections import namedtuple

class Clock(urwid.Text):

    def __init__(self, delegate, align="left"):
        self.delegate = delegate
        super(Clock, self).__init__("00:00", align=align)
        l = task.LoopingCall(self.start)
        l.start(1.0) # call every second

    def start(self):
        time = Clock.localTime()
        if ":" in self.text:
            delimiter = " "
        else:
            delimiter = ":"

        self.set_text("%s%s%s" % (time.hour, delimiter, time.minutes))
        self.delegate.shouldUpdateScreen()

    @classmethod
    def localTime(cls):
        """
        """
        timeStruct = time.localtime()
        # A value below 10 will not include the leading 0.
        hour = str(timeStruct.tm_hour) if timeStruct.tm_hour >= 10 else "0" + str(timeStruct.tm_hour)
        minutes = str(timeStruct.tm_min) if timeStruct.tm_min >= 10 else "0" + str(timeStruct.tm_min)
        seconds = str(timeStruct.tm_sec) if timeStruct.tm_sec >= 10 else "0" + str(timeStruct.tm_sec)
        LocalTime = namedtuple("localTime", "hour minutes seconds")

        return LocalTime(hour=hour, minutes=minutes, seconds=seconds)
