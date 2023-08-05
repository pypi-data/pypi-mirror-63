#
# Copyright (C) 2018-2020  Leo P. Singer <leo.singer@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import argparse
import logging
import sys

import slixmpp

from . import LVAlertClient, DEFAULT_SERVER


def parser():
    parser = argparse.ArgumentParser(prog='lvalert')
    parser.add_argument('-l', '--log', help='Log level', default='error',
                        choices='critical error warning info debug'.split())
    parser.add_argument('-n', '--netrc',
                        help='netrc file (default: read from NETRC '
                        'environment variable or ~/.netrc)')
    parser.add_argument('-r', '--resource',
                        help='XMPP resource (default: random)')
    parser.add_argument('-s', '--server', default=DEFAULT_SERVER,
                        help='LVAlert server hostname')
    parser.add_argument('-u', '--username',
                        help='User name (default: look up in netrc file)')

    subparsers = parser.add_subparsers(dest='action', help='sub-command help')
    subparsers.required = True

    subparser = subparsers.add_parser(
        'listen', help='Listen for LVAlert messages and print them to stdout.')

    subparser = subparsers.add_parser(
        'subscriptions', help='List your subscriptions')

    subparser = subparsers.add_parser(
        'nodes', help='List available pubsub nodes')

    subparser = subparsers.add_parser(
        'subscribe', help='Subscribe to one or more nodes')
    subparser.add_argument(
        'node', nargs='+', help='a pubsub node (e.g. cbc_gstlal)')

    subparser = subparsers.add_parser(
        'unsubscribe', help='Unsubscribe from one or more nodes')
    subparser.add_argument(
        'node', nargs='+', help='a pubsub node (e.g. cbc_gstlal)')

    return parser


def show(node, payload):
    print('Got item for node:', node)
    print(payload)
    print()


def main(args=None):
    opts = parser().parse_args(args)

    if opts.log is not None:
        logging.basicConfig(level=opts.log.upper())

    xmpp = LVAlertClient(username=opts.username,
                         resource=opts.resource,
                         server=opts.server,
                         netrc=opts.netrc,
                         interactive=True)

    xmpp.connect()

    if opts.action == 'listen':
        xmpp.listen(show)
    else:
        async def callback(*args):
            try:
                if opts.action == 'nodes':
                    print(*await xmpp.get_nodes(), sep='\n')
                elif opts.action == 'subscriptions':
                    print(*await xmpp.get_subscriptions(), sep='\n')
                elif opts.action == 'subscribe':
                    await xmpp.subscribe(*opts.node)
                elif opts.action == 'unsubscribe':
                    await xmpp.unsubscribe(*opts.node)
            except slixmpp.exceptions.IqError as e:
                print('XMPP error:', e.iq['error'], file=sys.stderr)
            finally:
                xmpp.stop()

        xmpp.add_event_handler('session_start', callback, disposable=True)

    xmpp.start()
