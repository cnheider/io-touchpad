#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" io-touchpad application.

This application will learn to associate symbols you draw on your touchpad
with certain actions you bound to those symbols.

Your finger's absolute position is fetched using a library called touchpadlib
which is based on evtest (version 1.32).

Source code encoding: UTF-8
"""

import _thread
import queue
import sys
import signal

from touchpadsignal import touchpadsignal
from signalcollection import signalcollection
from threads import application
from threads import listener



def handler(signum, frame):
    """Free memory after touchpad_signal_object when SIGINT call."""
    print("\nClosing the application...")
    if 'touchpad_signal_object' in globals():
        lib.erase_event(touchpad_signal_object)
    sys.exit(0)



# SIGINT signal handler.
signal.signal(signal.SIGINT, handler)

# Global variables.
queue = queue.Queue()
collection = signalcollection.SignalCollection()

# Run both threads.
print("\nUse your touchpad as usual. Have a nice day!")
listener.start(queue)
application.application_thread(collection, queue)
