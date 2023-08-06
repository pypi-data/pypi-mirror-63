#!/usr/bin/env python
#
# This file is part of zepl: https://gitlab.com/zepl1/zepl
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3
#
# parts of it are taken from pySerial. https://github.com/pyserial/pyserial
# (C)2002-2017 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause

import sys
import asyncio
import zmq.asyncio

from zepl.console import *
from zepl import UserIo

from threading import Thread

# super verbose websockets logging
#import logging
#logging.basicConfig(stream=sys.stdout)#, level=logging.DEBUG)
#logging.getLogger('websockets').setLevel(logging.DEBUG)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# default args can be used to override when calling main() from an other script
# e.g to create a zepl-my-device.py
def main(default_ip=None, default_port=8266, default_pw='asdf'):
    """Command line tool, entry point"""

    import argparse

    parser = argparse.ArgumentParser(
        description='Zepl - A simple remote terminal program for Micropython webREPL')

    parser.add_argument(
        'ip',
        nargs='?',
        help='hostname or ip',
        default=default_ip)

    parser.add_argument(
        'port',
        nargs='?',
        type=int,
        help=f'set port, default: {default_port}',
        default=default_port)

    group = parser.add_argument_group('data handling')

    group.add_argument(
        '-p', '--password',
        action='store',
        type=str,
        help='Password for WebREPL login',
        default=default_pw)

    group.add_argument(
        '--encoding',
        dest='serial_port_encoding',
        metavar='CODEC',
        help='set the encoding for the serial port (e.g. hexlify, Latin1, UTF-8), default: %(default)s',
        default='UTF-8')

    group.add_argument(
        '-f', '--filter',
        action='append',
        metavar='NAME',
        help='add text transformation',
        default=[])

    group.add_argument(
        '--eol',
        choices=['CR', 'LF', 'CRLF'],
        type=lambda c: c.upper(),
        help='end of line mode',
        default='CRLF')

    group.add_argument(
        '--raw',
        action='store_true',
        help='Do no apply any encodings/transformations',
        default=False)

    group = parser.add_argument_group('hotkeys')

    group.add_argument(
        '--menu-char',
        type=int,
        metavar='NUM',
        help=f'Unicode code of special character that is used as menu key, default: {key_description(chr(1))}',
        default=0x01)  # Menu: CTRL+A

    group.add_argument(
        '--exit-char',
        type=int,
        metavar='NUM',
        help=f'Unicode code of special character that is used as exit key, default: {key_description(chr(14))}',
        default=0x18)  # Menu: CTRL+X

    group = parser.add_argument_group('diagnostics')

    group.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress non-error messages',
        default=False)

    group.add_argument(
        '-d', '--dummy',
        action='store_true',
        help='load dummy protocol',
        default=False)

    args = parser.parse_args()

    if args.menu_char == args.exit_char:
        parser.error('--exit-char can not be the same as --menu-char')

    if args.filter:
        if 'help' in args.filter:
            sys.stderr.write('Available filters:\n')
            sys.stderr.write('\n'.join(
                '{:<10} = {.__doc__}'.format(k, v)
                for k, v in sorted(TRANSFORMATIONS.items())))
            sys.stderr.write('\n')
            sys.exit(1)
        filters = args.filter
    else:
        filters = ['default']

    cfg = {}
    cfg['dev_ip'] = args.ip
    cfg['dev_port'] = args.port
    cfg['dev_pw'] = args.password
    cfg['proto'] = 'WebREPL' # new!

    uri_dev_io = f'ipc://@{cfg["dev_ip"]}'

    zepl = UserIo(
        uri_dev_io,
        eol=args.eol.lower(),
        filters=filters)
    zepl.menu_character = unichr(args.menu_char)
    zepl.exit_character = unichr(args.exit_char)
    zepl.raw = args.raw
    zepl.set_rx_encoding(zepl.input_encoding)
    zepl.set_tx_encoding(zepl.output_encoding)

    if not args.quiet:
        sys.stderr.write(f'\
---  Quit: {key_description(zepl.menu_character)} followed by {key_description(zepl.exit_character)}\
  |  Help: {key_description(zepl.menu_character)} followed by h  ---\n')

    zepl.start()

    def dev_thread(uri_dev_io, cfg, dummy):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ctx = zmq.asyncio.Context()
        if dummy:
            from zepl_device.protocols.dummy import DummyIo
            io_runner = DummyIo(ctx, uri_dev_io, cfg)
        else:
            from zepl_device.protocols.webrepl import WebReplIo
            io_runner = WebReplIo(ctx, uri_dev_io, cfg)
        io_runner.start()
        loop.run_forever()
        io_runner.stop() # ??

    io_thread = Thread(target=dev_thread, name='io_runner', args=(uri_dev_io, cfg, args.dummy), daemon=True)
    io_thread.start()
    try:
        zepl.join(True)
        io_thread.join(True)
    except KeyboardInterrupt:
        pass
    if not args.quiet:
        sys.stderr.write('\n--- exit ---\n')

    zepl.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
