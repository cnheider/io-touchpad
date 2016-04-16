
import queue
import _thread
import sys
from ctypes import cdll

from touchpadsignal import touchpadsignal

LIB_DIRECTORY = "../lib"
TOUCHPADLIB_SHARED_LIBRARY = LIB_DIRECTORY + "/touchpadlib.so"

def start(queue):
    # Connect with touchpadlib.
    try:
        lib = cdll.LoadLibrary(TOUCHPADLIB_SHARED_LIBRARY)
    except OSError:
        print("No such library as touchpadlib.so.")
        sys.exit(1)

    touchpad_signal_object = lib.new_event()
    if touchpad_signal_object == 0:
        print("Cannot allocate memory in new_event.")
        lib.erase_event(touchpad_signal_object)
        sys.exit(1)

    fd = lib.initalize_touchpadlib_usage()
    if fd == -1:
        print("Touchpadlib initalize error.")
        lib.erase_event(touchpad_signal_object)
        sys.exit(1)

    _thread.start_new_thread(listener_thread, (queue, lib, fd, touchpad_signal_object))


def listener_thread(queue, lib, fd, touchpad_signal_object):
    """The main function of the listener thread.

    The listener thread fetches events from the touchpad and pushes them onto
    the queue.
    """
    while 1:
        if lib.fetch_touchpad_event(fd, touchpad_signal_object) == 1:
            print("Touchpad fetch error.")
            lib.erase_event(touchpad_signal_object)
            sys.exit(1)

        x = lib.get_x(touchpad_signal_object)
        y = lib.get_y(touchpad_signal_object)
        pressure = lib.get_pressure(touchpad_signal_object)
        seconds = lib.get_seconds(touchpad_signal_object)
        useconds = lib.get_useconds(touchpad_signal_object)

        time = combine_seconds_and_useconds(seconds, useconds)
        touchpad_signal = touchpadsignal.TouchpadSignal(x, y, pressure, time)
        queue.put(touchpad_signal, True)

def combine_seconds_and_useconds(seconds, useconds):
    """Combine seconds and miliseconds into one variable."""
    return seconds + 0.000001 * useconds
