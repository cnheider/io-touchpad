# -*- coding: utf-8 -*-

import signal
import sys
import threads.listener

def handler(signum, frame):
    """Free memory after touchpad_signal_object when SIGINT call."""
    print("\nClosing the application...")
    threads.listener.clean()
    sys.exit(0)

def setup():
    signal.signal(signal.SIGINT, handler)
