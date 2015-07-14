from time import time

from twisted.logger import Logger, LogPublisher
from twisted.protocols.basic import LineReceiver


class WabbitServer(LineReceiver):

    now = int(time())
    count = 0

    def lineReceived(self, line):
        now = int(time())
        if now - self.now == 1:
            self.now = now
            count, self.count = self.count, 0
            print count
        else:
            self.count += 1
        self.sendLine("received")
