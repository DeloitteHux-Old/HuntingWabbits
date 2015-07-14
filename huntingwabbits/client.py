"""
"""
import argparse
import re
import sys

from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString, connectProtocol
from twisted.protocols.basic import LineReceiver
from twisted.logger import textFileLogObserver

from huntingwabbits import __version__


parser = argparse.ArgumentParser(
    description="Interface to the VW optimization models.",
    epilog=re.sub(":\w+:", "", __doc__),  # strip out Sphinx refs
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("-V", "--version", action="version", version=__version__)
parser.add_argument(
    "endpoint",
    help="the endpoint to listen on for URLs",
)


class BenchmarkClient(LineReceiver):
    def lineReceived(self, line):
        assert line == "received"
        self.sendLine("request")


def main(reactor=reactor):
    arguments = vars(parser.parse_args())
    endpoint = clientFromString(
        reactor=reactor,
        description=arguments["endpoint"],
    )

    connectProtocol(endpoint, BenchmarkClient()).addCallback(
        lambda protocol : protocol.sendLine("request"),
    )
    reactor.run()
