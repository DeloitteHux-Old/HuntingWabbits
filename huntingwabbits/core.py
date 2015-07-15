from time import time

from twisted.logger import Logger, LogPublisher
from twisted.protocols.basic import LineReceiver
from huntingwabbits.vw import EmptyVWModel, VWCFFIWrapper


class WabbitServer(LineReceiver):

    now = int(time())
    count = 0
    vw = EmptyVWModel()

    def lineReceived(self, line):
        if not isinstance(self.vw, VWCFFIWrapper):
            self.vw = VWCFFIWrapper("/usr/bin/vw -b24 -t -i /Users/vvlad/tmp/vw_hm/model.vw --quiet")
        now = int(time())
        if now - self.now >= 1:
            self.now = now
            count, self.count = self.count, 0
            print count
        else:
            self.count += 1
        self.sendLine("received %s" % self.vw.getScore(line))
