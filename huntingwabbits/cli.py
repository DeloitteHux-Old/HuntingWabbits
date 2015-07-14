"""
"""
import argparse
import re
import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import serverFromString
from twisted.logger import textFileLogObserver

from huntingwabbits import __version__
from huntingwabbits.core import WabbitServer


parser = argparse.ArgumentParser(
    description="Interface to the VW optimization models.",
    epilog=re.sub(":\w+:", "", __doc__),  # strip out Sphinx refs
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("-V", "--version", action="version", version=__version__)
parser.add_argument(
    "endpoint",
    nargs="+",
    help="the endpoint to listen on for URLs",
)


def main(reactor=reactor):
    arguments = vars(parser.parse_args())
    for description in arguments["endpoint"]:
        endpoint = serverFromString(
            reactor=reactor,
            description=description,
        )

        wabbit = Factory.forProtocol(WabbitServer)
        endpoint.listen(wabbit)
    reactor.run()
