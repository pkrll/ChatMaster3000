import urwid
from twisted.internet import task
from support.helpers import localTime

class Clock(urwid.Text):

    def __init__(self, delegate, align="left"):
        self.delegate = delegate
        super(Clock, self).__init__("00:00", align=align)
        l = task.LoopingCall(self.start)
        l.start(1.0) # call every second

    def start(self):
        time = localTime()
        if ":" in self.text:
            delimiter = " "
        else:
            delimiter = ":"

        self.set_text("%s%s%s" % (time.hour, delimiter, time.minutes))
        self.delegate.shouldUpdateScreen()
