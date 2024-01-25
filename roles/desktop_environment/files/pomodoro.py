#!/usr/bin/env python3

import argparse
import configparser
import math
import os
import signal
import socket
from subprocess import check_call, DEVNULL, STDOUT
import sys
import threading
import time


class PomodoroError(Exception):
    pass


running = True
seconds_left = 0
BUFFER_BYTES = 1024


def main():
    global running
    global seconds_left
    euid = os.geteuid()
    socket_path = f"/tmp/pomodoro_{euid}"
    signal.signal(signal.SIGINT, sigint_handler)
    command, seconds_left, configfile = parse_command()
    config = parse_config(configfile)
    if command == 'start':
        run_pomodoro(config, socket_path)
    else:
        process_command(socket_path, command)


def sigint_handler(sig, frame):
    """Cleans up after a CTRL-C"""
    euid = os.geteuid()
    socket_path = f"/tmp/pomodoro_{euid}"
    if os.path.exists(socket_path):
        os.unlink(socket_path)
    sys.exit(0)


def parse_command() -> list[str, int, str]:
    """Function returns the command & seconds remaining from program args."""
    parser = argparse.ArgumentParser(
        description=('Countdown a timer in the background and communicate '
                     'with it')
    )
    parser.add_argument('command', metavar='command', type=str,
                        help='any of <start, status, cancel>'
    )
    parser.add_argument('minutes', metavar='M', type=int, nargs='?',
                        default=25, help='number of minutes')
    parser.add_argument('--config', metavar='PATH', type=str,
                        default=os.path.join('.','pomodoro.ini'),
                        help='path to configuration files'
    )
    args = parser.parse_args()
    if args.command == 'start':
        seconds = args.minutes * 60
    else:
        seconds = 0
    return args.command, seconds, args.config


def parse_config(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def run_pomodoro(config, socket_path):
    """Procedure set the pomodoro going as a background process."""
    global running
    global seconds_left
    if os.path.exists(socket_path):
        print('Timer already running. Exiting.')
        sys.exit(1)
    if os.fork():
        sys.exit()
    server = set_socket(socket_path)
    countdown = threading.Thread(target=listen, args=(server,), daemon=True)
    countdown.start()
    while running and seconds_left > 0:
        time.sleep(1)
        seconds_left -= 1
    os.unlink(socket_path)
    if seconds_left <= 0:
        play_alarm(config)


def play_alarm(config):
    if config['sound']['sound'] == 'on':
        check_call([config['sound']['player'], config['sound']['alarm']],
                   stdout=DEVNULL, stderr=STDOUT)


def set_socket(socket_path):
    try:
        os.unlink(socket_path)
    except OSError:
        if os.path.exists(socket_path):
            raise PomodoroError
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    server.listen(1)
    return server


def listen(server):
    """Procedure infinitely processes client commands"""
    global seconds_left
    jump = {
        'status': send_remaining,
        'cancel': cancel_timer,
        '': close_connection
    }
    while True:
        connection, client_address = server.accept()
        with connection:
            while True:
                data = connection.recv(BUFFER_BYTES).decode()
                if data == '':
                    close_connection(connection)
                    break
                try:
                    if data in jump:
                        jump[data](connection)
                    else:
                        connection.sendall(b'Error')
                except BrokenPipeError:
                    connection.close()
                    break


def send_remaining(connection):
    """Procedure sends min:sec remaining through socket"""
    min, sec = sec_to_time(seconds_left)
    msg = f"{min:02}:{sec:02}"
    connection.sendall(msg.encode())


def sec_to_time(seconds:int) -> list[int, int]:
    """Function converts seconds to minutes, seconds"""
    min = math.floor(seconds / 60)
    sec = seconds % 60
    return min, sec


def cancel_timer(connection):
    global running
    running = False
    connection.sendall('cancelled'.encode())


def close_connection(connection):
    connection.shutdown(0)
    connection.close()


def process_command(socket_path, command):
    """Procedure prints remaining pomodoro time from daemon."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        try:
            s.connect(socket_path)
        except FileNotFoundError:
            print('none')
            sys.exit(0)
        except ConnectionRefusedError:
            print('stalled')
            sys.exit(0)
        s.sendall(command.encode())
        print(s.recv(BUFFER_BYTES).decode())
        s.shutdown(1)
        s.close()


if __name__ == '__main__':
    main()
