# -*- coding: utf-8 -*-

import sys
import _thread
from ctypes import cdll, Structure, c_long, POINTER

LIB_DIRECTORY = "../lib"
TOUCHPADLIB_SHARED_LIBRARY = LIB_DIRECTORY + "/touchpadlib.so"

class TouchpadEvent(Structure):
    """The Pythonic version of the touchpad_event struct."""

    _fields_ = [("x", c_long),
                ("y", c_long),
                ("pressure", c_long),
                ("seconds", c_long),
                ("useconds", c_long)]

class TouchpadSpecification(Structure):

    _fields_ = [("min_x", c_long),
                ("max_x", c_long),
                ("min_y", c_long),
                ("max_y", c_long),
                ("min_pressure", c_long),
                ("max_pressure", c_long)]

class Touchpadlib:

    touchpadlib = None
    touchpad_event = None
    touchpad_specification = None
    touchpad_file_descriptor = None

    @classmethod
    def get_event(cls):
        cls.initialize()
        cls.fetch_touchpad_event()
        return { 'x': cls.touchpad_event.contents.x,
                 'y': cls.touchpad_event.contents.y,
                 'pressure': cls.touchpad_event.contents.pressure,
                 'seconds': cls.touchpad_event.contents.seconds,
                 'useconds': cls.touchpad_event.contents.useconds }

    @classmethod
    def get_specification(cls):
        cls.initialize()
        cls.fetch_touchpad_specification()
        contents = cls.touchpad_specification.contents
        return { 'min_x': contents.min_x,
                 'max_x': contents.max_x,
                 'min_y': contents.min_y,
                 'max_y': contents.max_y,
                 'min_pressure': contents.min_pressure,
                 'max_pressure': contents.max_pressure }

    @classmethod
    def initialize(cls):
        """Initialize the static variables."""
        if cls.touchpadlib is None:
            cls.conncect_to_library()
        if cls.touchpad_event is None:
            cls.create_touchpad_event()
        if cls.touchpad_file_descriptor is None:
            cls.initialize_touchpadlib()
        if cls.touchpad_specification is None:
            cls.create_touchpad_specification()

    @classmethod
    def conncect_to_library(cls):
        """Conncet to the touchpadlib."""
        try:
            cls.touchpadlib = cdll.LoadLibrary(TOUCHPADLIB_SHARED_LIBRARY)
        except OSError:
            print("ERROR: No such library as touchpadlib.so.")
            cls.interrupt_and_finish()

    @classmethod
    def create_touchpad_event(cls):
        """Get a C language struct from the touchpadlib."""
        cls.touchpadlib.new_event.restype = POINTER(TouchpadEvent)
        cls.touchpad_event = cls.touchpadlib.new_event()
        if cls.touchpad_event == 0:
            print("ERROR: Cannot allocate memory in new_event().")
            cls.interrupt_and_finish()

    @classmethod
    def create_touchpad_specification(cls):
        cls.touchpadlib.new_specification.restype = \
            POINTER(TouchpadSpecification)
        cls.touchpad_specification = cls.touchpadlib.new_specification()
        if cls.touchpad_specification == 0:
            print("ERROR: Cannto allocate memory in new_specification().")
            cls.interrupt_and_finish()

    @classmethod
    def free_touchpad_event(cls):
        """Free the memory allocated for the touchpad_event."""
        cls.touchpadlib.free_event(cls.touchpad_event)

    @classmethod
    def free_touchpad_specification(cls):
        """Free the memory allocated for the touchpad_event."""
        cls.touchpadlib.free_specification(cls.touchpad_specification)

    @classmethod
    def initialize_touchpadlib(cls):
        """Initialize the touchpadlib library.

        Set the touchpad_file_descriptor.
        """
        cls.touchpad_file_descriptor = \
            cls.touchpadlib.initialize_touchpadlib_usage()
        if cls.touchpad_file_descriptor == -1:
            print("ERROR: touchpadlib initialize error.")
            cls.interrupt_and_finish()

    @classmethod
    def fetch_touchpad_event(cls):
        """Fetch the next event from the touchpad."""
        if cls.touchpadlib.fetch_touchpad_event(cls.touchpad_file_descriptor,
                                                cls.touchpad_event) == 1:
            print("ERROR: touchpadlib fetch error.")
            cls.interrupt_and_finish()

    @classmethod
    def fetch_touchpad_specification(cls):
        if cls.touchpadlib.fetch_touchpad_specification(
                cls.touchpad_file_descriptor, cls.touchpad_specification) != 0:
            print("ERROR: Can't get the touchpad specification.")
            cls.interrupt_and_finish()

    @classmethod
    def clean(cls):
        """Securily free the touchpad_event.

        A function for other modules to be able to free the touchpad_event
        in an emergency.

        terminationhandler uses it.
        """
        if cls.touchpad_event is not None:
            cls.free_touchpad_event()
        if cls.touchpad_specification is not None:
            cls.free_touchpad_specification()

    @classmethod
    def interrupt_and_finish(cls):
        """Interrupt the main thread and exit.

        Clean the C language data structures.

        Exit thread with the exit code of 1.
        """
        cls.clean()
        _thread.interrupt_main()
        sys.exit(1)

