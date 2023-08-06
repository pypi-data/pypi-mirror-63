"""
Logger with thread storage to add to log information about request.

Use main_thread/sending/receiving to switch logger modes.
"""
import threading
import logging
from bombard.terminal_colours import OFF, GRAY
from typing import Optional
from bombard.pretty_ns import time_ns, pretty_ns as plain_ns


log = logging.getLogger()
thread_data = threading.local()
pretty_ns = plain_ns  # we can redefine that to have customized formatting


def main_thread():
    """
    We are in main thread
    """
    thread_data.thread_id = 'Main'
    thread_data.request_id = ''
    thread_data.request_name = ''
    thread_data.dir = ''
    thread_data.start = None
    thread_data.colour = OFF


def sending(thread_id, request_id, request_name):
    """
    Start sending request
    """
    thread_data.thread_id = thread_id
    thread_data.request_id = request_id
    thread_data.request_name = request_name
    thread_data.dir = '>' * 3
    thread_data.colour = GRAY
    thread_data.start = time_ns()


def receiving():
    """
    Got response to request
    """
    thread_data.dir = '<' * 3
    thread_data.colour = OFF


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.threadid = thread_data.thread_id
        record.requestid = str(thread_data.request_id).rjust(4)
        record.colour = thread_data.colour
        record.requestname = thread_data.request_name
        record.dir = thread_data.dir
        record.elapsed = pretty_ns(time_ns() - thread_data.start) if thread_data.start is not None else ''
        return super().format(record)


def setup_logging(level: int, log_file_name: Optional[str] = None):
    main_thread()
    handler = logging.StreamHandler()
    formatter = RequestFormatter(
            fmt=f'%(colour)s%(asctime)s %(requestid)s %(elapsed)s (thread %(threadid)s) '
                f'%(requestname)s %(dir)s %(message)s{OFF}',
            datefmt='%d %b %H:%M:%S'
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    log.handlers = []
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    if log_file_name is not None:
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        log.addHandler(file_handler)
