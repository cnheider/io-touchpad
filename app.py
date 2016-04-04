#!/usr/bin/env python3

# Encoding: UTF-8

import _thread
import queue
import time
import signal
import sys
from ctypes import cdll

MAX_NUMBER_OF_POINTS_IN_GROUP = 3000
MAX_DURATION_OF_GROUP = 4
MAX_BREAK_BETWEEN_TWO_SIGNALS = 0.3


class TouchpadSignal:
    """Wrapper for the struct touchpad_event from touchpadlib.

    :param x
    :param y
    :param pressure
    :param time
    """

    def __init__(self, x, y, pressure, time):
        self.x = x
        self.y = y
        self.pressure = pressure
        self.time = time

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_time(self):
        return self.time

    def is_it_stop_signal(self):
        # TODO Implement this method.
        # We could set condition pressure<1 but for now the only reason
        # to end the group is a long break between signals.
        return False

    def is_it_proper_signal_of_point(self):
        return self.x >= 0 and self.y >= 0

# Signal queue.
queue = queue.Queue()

# Connecting with touchpadlib.
lib = cdll.LoadLibrary('./lib/touchpadlib.so') # TODO error handle
touchpad_signal_object = lib.new_event()
fd = lib.initalize_touchpadlib_usage() # TODO error handle


def handler(signum, frame):
    """Free memory after touchpad_signal_object when SIGINT call."""
    print("");
    print("ending...")
    lib.erase_event(touchpad_signal_object)
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


def combine_seconds_and_useconds(seconds, useconds):
    """Combine seconds and miliseconds into one variable."""
    return seconds + 0.000001 * useconds


def listener_thread() :
    """The main function of the listener thread.

    The listener thread fetches events from the touchpad and pushes them onto
    the queue.
    """
    while 1:
        lib.fetch_touchpad_event(fd, touchpad_signal_object) # TODO error handle
        x        = lib.get_x(touchpad_signal_object)
        y        = lib.get_y(touchpad_signal_object)
        pressure = lib.get_pressure(touchpad_signal_object)
        seconds  = lib.get_seconds(touchpad_signal_object)
        useconds = lib.get_useconds(touchpad_signal_object)

        time = combine_seconds_and_useconds(seconds, useconds)
        touchpad_signal = TouchpadSignal(x, y, pressure, time)
        queue.put(touchpad_signal, True)


def send_points_to_interpreter(signal_list):
    """Interpret the signals from the signal list.

    At the moment the function is not interpreting anything. It just prints the
    first 10 points/events/signals from the signal_list.

    :param signal_list: List of read events.
    """
    if not signal_list:
        return
    print ("new portion of points:")
    counter = 0
    le = len(signal_list)
    for one_signal in signal_list:
        counter += 1
        if counter == 11:
            print("...")
            break
        print ("%d / %d x: %d y: %d" % (counter, le, one_signal.get_x(), one_signal.get_y() ) )
    print()


class SignalCollection:
    """Collection of signals (points) to interpret."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.signal_list = []

    def need_to_remove_first_signal_from_list(self, touchpad_signal_to_add):
        if not self.signal_list:
            return False
        if len(self.signal_list) >= MAX_NUMBER_OF_POINTS_IN_GROUP:
            return True
        if touchpad_signal_to_add.get_time() - self.signal_list[0].get_time() > MAX_DURATION_OF_GROUP:
            return True
        return False

    def add_new_signal_and_remove_too_old_signals(self, touchpad_signal):
        while self.need_to_remove_first_signal_from_list(touchpad_signal):
            self.signal_list.pop(0)
        self.signal_list.append(touchpad_signal)

    def too_much_time_passed(self, new_signal_time):
        if self.signal_list and new_signal_time - self.signal_list[-1].get_time() > MAX_BREAK_BETWEEN_TWO_SIGNALS:
            return True
        return False

    def as_list(self):
        return self.signal_list


signal_collection = SignalCollection()


def application_thread():
    """The application thread.

    It receives signals/events from the listener thread using a queue and then
    interprets the data.
    """
    # main loop - in every iteration one signal is read, or too long break in signal streaming is captured
    while 1:
        while queue.empty() and not signal_collection.too_much_time_passed(time.time()):
            pass

        is_new_signal = not (queue.empty())

        if is_new_signal:
            touchpad_signal = queue.get()

        if not(is_new_signal) or touchpad_signal.is_it_stop_signal():
            send_points_to_interpreter(signal_collection.as_list())
            signal_collection.reset()
        elif signal_collection.too_much_time_passed(touchpad_signal.get_time()):
            send_points_to_interpreter(signal_collection.as_list())
            signal_collection.reset()
            if touchpad_signal.is_it_proper_signal_of_point():
                signal_collection.add_signal_and_remove_too_old_signals(touchpad_signal)
        else:
            if touchpad_signal.is_it_proper_signal_of_point():
                signal_collection.add_new_signal_and_remove_too_old_signals(touchpad_signal)


# Run both threads.

_thread.start_new_thread(listener_thread, () )
application_thread()
