# -*- coding: utf-8 -*-

"""Tests for touchpad signal """

import pytest

from touchpadsignal import touchpadsignal 

#i am doing it to omit INIT invokation
touchpad = touchpadsignal.TouchpadSignal.__new__(touchpadsignal.TouchpadSignal)

def test_combine_seconds_and_useconds():
    assert touchpad.combine_seconds_and_useconds(10,234) == 10 + 0.000001 * 234

def test_get_x():
    touchpad.x_value = 5
    assert touchpad.get_x() == 5

def test_get_y():
    touchpad.y_value = 6
    assert touchpad.get_y() == 6

def test_get_time():
    touchpad.time = 11
    assert touchpad.get_time() == 11

def test_get_pressure():
    touchpad.pressure = 0.10123
    assert touchpad.get_pressure() == 0.10123

