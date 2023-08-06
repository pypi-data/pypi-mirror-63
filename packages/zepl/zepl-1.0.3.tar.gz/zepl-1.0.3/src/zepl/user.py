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

from __future__ import absolute_import

import codecs, struct, os, sys
import threading
import zmq

from .console import *

class UserIo():
    """\
    Terminal application. Copy data from console to micropthon WebREPL and vice versa.
    Handle special keys from the console to show menu etc.
    """

    def __init__(self, uri_dev_io, eol='crlf', filters=()):
        ctx = zmq.Context()

        self.uri_dev_io = uri_dev_io

        self.uri_dev_in = f'inproc://dev_in'
        self.uri_dev_out = f'inproc://dev_out'

        self.user_in = ctx.socket(zmq.PAIR)
        self.user_out = ctx.socket(zmq.PAIR)

        self.dev_in = ctx.socket(zmq.PAIR)
        self.dev_out = ctx.socket(zmq.PAIR)

        self.z_sock = ctx.socket(zmq.PAIR)

        self.poller = zmq.Poller()
        self.poller.register(self.dev_in, zmq.POLLIN)
        self.poller.register(self.z_sock, zmq.POLLIN)

        self.console = Console()
        self.raw = False
        self.input_encoding = 'UTF-8'
        self.output_encoding = 'UTF-8'
        self.eol = eol
        self.filters = filters
        self.update_transformations()
        self.menu_character = unichr(0x01)  # 'default': CTRL+A
        self.exit_character = unichr(0x18)  # 'default': CTRL+X
        self.rx_decoder = None
        self.tx_decoder = None

        self.mp_codec_fname = ''

    def _start_relay(self):
        """Start relay thread"""
        self._relay_alive = True
        # connect/bind to zmq sockets
        self.dev_in.bind(self.uri_dev_in)
        self.dev_out.bind(self.uri_dev_out)
        self.z_sock.connect(self.uri_dev_io)
        # start relay
        self.relay_thread = threading.Thread(target=self.relay, name='relay', daemon=True)
        self.relay_thread.start()

    def _start_writer(self):
        """Start writer thread"""
        self._writer_alive = True
        self.user_in.connect(self.uri_dev_in)
        # start console->zmq thread
        self.writer_thread = threading.Thread(target=self.writer, name='tx', daemon=True)
        self.writer_thread.start()

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        self.user_out.connect(self.uri_dev_out)
        # start zmq->console thread
        self.reader_thread = threading.Thread(target=self.reader, name='rx', daemon=True)
        self.reader_thread.start()

    def start(self):
        """start worker threads"""
        self._start_relay()
        self._start_writer()
        self._start_reader()

        self.console.setup()

    def stop(self):
        """set flag to stop worker threads"""
        self._reader_alive = False
        self._writer_alive = False
        self._relay_alive  = False

    def join(self, read_only=False):
        """wait for worker threads to terminate"""
        self.writer_thread.join()
        if not read_only:
            self.reader_thread.join()
        self.relay_thread.join()
        # cleanup zmq sockets
        self.dev_in.close()
        self.dev_out.close()
        self.z_sock.close()

    def close(self):
        pass

    def writer(self):
        """loop and copy console->zmq until self.exit_character character is found.
        When self.menu_character is found, interpret the next key locally.
        """
        menu_active = False
        try:
            while self._writer_alive:
                try:
                    c = self.console.getkey()
                except KeyboardInterrupt:
                    c = '\x03'
                if not self._writer_alive:
                    break
                if menu_active:
                    self.handle_menu_key(c)
                    menu_active = False
                elif c == self.menu_character:
                    menu_active = True      # next char will be for menu
                else:
                    #~ if self.raw:
                    text = c
                    for transformation in self.tx_transformations:
                        text = transformation.tx(text)
                    msg = [ b'c', self.tx_encoder.encode(text)]
                    self.user_in.send_multipart(msg)
        except:
            self._writer_alive = False
            raise

    def reader(self):
        """loop and copy zmq->console"""
        try:
            while self._reader_alive:
                _, data = self.user_out.recv_multipart()
                if data:
                    if self.raw:
                        self.console.write_bytes(data)
                    else:
                        text = self.rx_decoder.decode(data)
                        for transformation in self.rx_transformations:
                            text = transformation.rx(text)
                        self.console.write(text)
        except Exception:
            raise       # XXX handle instead of re-raise?

    def relay(self):
        """Relays between websockets<-->console
        """
        while self._relay_alive:
            socks = dict(self.poller.poll(1000))

            if self.dev_in in socks.keys():
                # data from console
                msg = self.dev_in.recv_multipart()
                self.z_sock.send_multipart(msg)

            if self.z_sock in socks.keys():
                # data from websocket
                msg = self.z_sock.recv_multipart()
                self.dev_out.send_multipart(msg)

    def update_transformations(self):
        """take list of transformation classes and instantiate them for rx and tx"""
        transformations = [EOL_TRANSFORMATIONS[self.eol]] + [TRANSFORMATIONS[f]
                                                             for f in self.filters]
        self.tx_transformations = [t() for t in transformations]
        self.rx_transformations = list(reversed(self.tx_transformations))

    def set_rx_encoding(self, encoding, errors='replace'):
        """set encoding for received data"""
        self.input_encoding = encoding
        self.rx_decoder = codecs.getincrementaldecoder(encoding)(errors)

    def set_tx_encoding(self, encoding, errors='replace'):
        """set encoding for transmitted data"""
        self.output_encoding = encoding
        self.tx_encoder = codecs.getincrementalencoder(encoding)(errors)

    def handle_menu_key(self, c):
        """Implement a simple menu / settings"""
        if c == self.menu_character:
            # Menu character again -> send itself
            self.user_in.send_multipart([b'c', self.tx_encoder.encode(c)])
            pass
        elif c in self.exit_character:
            self.stop()
            pass
        elif c in '\x08hH?':
            # CTRL+H, h, H, ? -> Show help
            sys.stderr.write(self.get_help_text())
        elif c in 'rR':
            # r, R -> send machine reset sequence
            self.machine_reset()
        elif c in 'vV':
            # v, V -> get and print version
            self.get_ver()
        elif c in 'uU':
            # u, U -> upload file
            self.upload_file()
        elif c in 'dD':
            # d, D -> download file
            self.download_file()
        elif c in 'lL':
            # l, L -> send ls sequence
            self.list_files()
        elif c == '\x06':
            # CTRL+F -> edit filters
            self.change_filter()
        elif c == '\x0c':
            # CTRL+L -> EOL mode
            modes = list(EOL_TRANSFORMATIONS)   # keys
            eol = modes.index(self.eol) + 1
            if eol >= len(modes):
                eol = 0
            self.eol = modes[eol]
            sys.stderr.write('--- EOL: {} ---\n'.format(self.eol.upper()))
            self.update_transformations()
        elif c == '\x05':
            # CTRL+E -> set encoding
            self.change_encoding()
        else:
            sys.stderr.write('--- unknown menu character {} --\n'.format(key_description(c)))

    def download_file(self):
        """Ask user for filenname and send its contents"""
        sys.stderr.write('\n--- File to download: ')
        sys.stderr.flush()
        with self.console:
            filename = sys.stdin.readline().rstrip('\r\n')
            if filename:
                try:
                    self.user_in.send_multipart([b'mp', b'get', filename.encode()])
                    self.mp_codec_fname = filename
                except IOError as e:
                    sys.stderr.write('--- ERROR opening file {}: {} ---\n'.format(filename, e))
        pass

    def upload_file(self):
        """Ask user for filenname and send its contents"""
        sys.stderr.write('\n--- File to upload: ')
        sys.stderr.flush()
        with self.console:
            filename = sys.stdin.readline().rstrip('\r\n')
            if filename:
                try:
                    fsize = os.stat(filename)[6]
                    with open(filename, 'rb') as f:
                        sys.stderr.write('--- Sending file {} ---\n'.format(filename))
                        while True:
                            block = f.read(fsize)
                            if not block:
                                break
                            cmd_seq = [b'mp', b'put', filename.encode(), f'{fsize}'.encode(), block]
                            self.user_in.send_multipart(cmd_seq)
                            sys.stderr.write('.')   # Progress indicator.
                    sys.stderr.write('\n--- File {} sent ---\n'.format(filename))
                except IOError as e:
                    sys.stderr.write('--- ERROR opening file {}: {} ---\n'.format(filename, e))

    def machine_reset(self):
        self.user_in.send_multipart([b'c', b'\x03import machine; machine.reset()\r\n'])

    def get_ver(self):
        self.user_in.send_multipart([b'mp', b'cmd', b'ver'])

    def list_files(self):
        self.user_in.send_multipart([b'c', b'\x03import os; os.listdir()\r\n'])

    def change_filter(self):
        """change the i/o transformations"""
        sys.stderr.write('\n--- Available Filters:\n')
        sys.stderr.write('\n'.join(
            '---   {:<10} = {.__doc__}'.format(k, v)
            for k, v in sorted(TRANSFORMATIONS.items())))
        sys.stderr.write('\n--- Enter new filter name(s) [{}]: '.format(' '.join(self.filters)))
        with self.console:
            new_filters = sys.stdin.readline().lower().split()
        if new_filters:
            for f in new_filters:
                if f not in TRANSFORMATIONS:
                    sys.stderr.write('--- unknown filter: {!r}\n'.format(f))
                    break
            else:
                self.filters = new_filters
                self.update_transformations()
        sys.stderr.write('--- filters: {}\n'.format(' '.join(self.filters)))

    def change_encoding(self):
        """change encoding on the serial port"""
        sys.stderr.write('\n--- Enter new encoding name [{}]: '.format(self.input_encoding))
        with self.console:
            new_encoding = sys.stdin.readline().strip()
        if new_encoding:
            try:
                codecs.lookup(new_encoding)
            except LookupError:
                sys.stderr.write('--- invalid encoding name: {}\n'.format(new_encoding))
            else:
                self.set_rx_encoding(new_encoding)
                self.set_tx_encoding(new_encoding)
        sys.stderr.write('--- serial input encoding: {}\n'.format(self.input_encoding))
        sys.stderr.write('--- serial output encoding: {}\n'.format(self.output_encoding))

    def get_help_text(self):
        """return the help text"""
        # help text, starts with blank line!
        return f"""
--- zmq ({zmq.__version__}) - zepl - help
---
--- Micropython hotkeys
--- {key_description(chr(3))} Micropython Keyboard Interrupt
--- {key_description(chr(4))} Micropython Soft Reset
---
--- {key_description(self.menu_character)} Menu escape key
--- Menu keys:
---    {key_description(self.menu_character)} Send the menu character itself to remote
---    {key_description(self.exit_character)} Exit program
---    {key_description(chr(5))} encoding
---    {key_description(chr(6))} edit filters
---    {key_description(chr(12))} EOL mode
---    h Show help
---    r Micropython Machine Reset
---    v Get Version
---    l List files
---    u Upload file (prompt will be shown)
---    d Download file (prompt will be shown)
"""
