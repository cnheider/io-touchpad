# -*- coding: utf-8 -*-
import sys
from ctypes import cdll

LIB_DIRECTORY = "../lib"
TOUCHPADLIB_SHARED_LIBRARY = LIB_DIRECTORY + "/touchpadlib.so"

class TouchpadSignal:
    """Wrapper for the struct touchpad_event from touchpadlib.

    :param x
    :param y
    :param pressure
    :param time
    """

    touchpadlib = None
    touchpad_event = None
    touchpad_file_descriptor = None

    def __init__(self):
        TouchpadSignal.initialize()
        TouchpadSignal.fetch_touchpad_event()

        touchpadlib = TouchpadSignal.touchpadlib
        touchpad_event = TouchpadSignal.touchpad_event

        self.x_value = touchpadlib.get_x(touchpad_event)
        self.y_value = touchpadlib.get_x(touchpad_event)
        self.pressure = touchpadlib.get_pressure(touchpad_event)
        seconds = touchpadlib.get_seconds(touchpad_event)
        useconds = touchpadlib.get_useconds(touchpad_event)
        self.time = self.combine_seconds_and_useconds(seconds, useconds)

    def get_x(self):
        return self.x_value

    def get_y(self):
        return self.y_value

    def get_time(self):
        return self.time

    def is_it_stop_signal(self):
        # TODO Implement this method. Not in the first iteration.
        # We could set condition pressure<1 but for now the only reason
        # to end the group is a long break between signals.
        return False

    def is_it_proper_signal_of_point(self):
        return self.x_value >= 0 and self.y_value >= 0

    @classmethod
    def initialize(cls):
        if cls.touchpadlib is None:
            cls.conncect_to_library()
        if cls.touchpad_event is None:
            cls.create_touchpad_event()
        if cls.touchpad_file_descriptor is None:
            cls.initialize_touchpadlib()

    @classmethod
    def conncect_to_library(cls):
        # Connect with touchpadlib.
        try:
            cls.touchpadlib = cdll.LoadLibrary(TOUCHPADLIB_SHARED_LIBRARY)
        except OSError:
            print("ERROR: No such library as touchpadlib.so.")
            sys.exit(1)

    @classmethod
    def create_touchpad_event(cls):
        cls.touchpad_event = cls.touchpadlib.new_event()
        if cls.touchpad_event == 0:
            print("ERROR: Cannot allocate memory in new_event().")
            cls.free_touchpad_event()
            sys.exit(1)

    @classmethod
    def free_touchpad_event(cls):
        cls.touchpadlib.erase_event(cls.touchpad_event)

    @classmethod
    def initialize_touchpadlib(cls):
        cls.touchpad_file_descriptor = cls.touchpadlib.initalize_touchpadlib_usage()
        if cls.touchpad_file_descriptor == -1:
            print("ERROR: touchpadlib initalize error.")
            cls.free_touchpad_event()
            sys.exit(1)

    @classmethod
    def fetch_touchpad_event(cls):
        touchpadlib = cls.touchpadlib
        file_descriptor = cls.touchpad_file_descriptor
        if touchpadlib.fetch_touchpad_event(file_descriptor, \
                cls.touchpad_event) == 1:
            print("ERROR: touchpadlib fetch error.")
            cls.free_touchpad_event()
            sys.exit(1)

    @classmethod
    def clean(cls):
        if cls.touchpad_event != None:
            cls.free_touchpad_event()

    @staticmethod
    def combine_seconds_and_useconds(seconds, useconds):
        """Combine seconds and miliseconds into one variable."""
        return seconds + 0.000001 * useconds
