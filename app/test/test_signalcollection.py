# -*- coding: utf-8 -*-

"""Tests for signal collection """

import pytest

from signalcollection import signalcollection

collection = signalcollection.SignalCollection()

def test_init():
    """Test for initial function"""
    assert collection.signal_list == []


def test_reset():
    """Test for reseting signal list"""
    collection.signal_list = [5]
    assert collection.signal_list == [5]

    collection.reset()
    assert collection.signal_list == []

def test__is_to_big():
    """Test _is_too_big function"""
    maxi = signalcollection.MAX_NUMBER_OF_SIGNALS_IN_GROUP

    for i in range(0,maxi-1):
        collection.signal_list.append(i)

    assert collection._is_too_big() == False

    collection.signal_list.append(-1)

    assert collection._is_too_big() == True


def test__is_empty():
    """Test _is_empty function"""
    collection.signal_list = [5]
    assert collection._is_empty() == False

    collection.reset()
    assert collection._is_empty() == True

def test_as_list():
    """Test as_empty function"""
    assert collection.as_list() == collection.signal_list

class signal_for_test():

    def __init__(self):
        self.time = 0

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

def test_is_head_too_old():
    """Test is_head_too_old function"""

    #we put signal with time 0
    signal_zero = signal_for_test()

    collection.signal_list.append(signal_zero)

    signal_maxi = signal_for_test()
    signal_maxi.set_time(signalcollection.MAX_DURATION_OF_GROUP)

    assert collection._is_head_too_old(signal_maxi) == False

    signal_maxi.set_time(signalcollection.MAX_DURATION_OF_GROUP+0.1)

    assert collection._is_head_too_old(signal_maxi) == True

    collection.reset()

def test_is_recent_enough():
    """Test is_recent_enough function"""

    #we put signal with time 0
    signal_zero = signal_for_test()

    collection.signal_list.append(signal_zero)

    assert collection.is_recent_enough(signalcollection.MAX_BREAK_BETWEEN_TWO_SIGNALS) == True
    assert collection.is_recent_enough(signalcollection.MAX_BREAK_BETWEEN_TWO_SIGNALS+0.1) == False

    collection.reset()

def test__need_to_remove_head():
    """Test need_to_remove_head function"""

    #we put signal with time 0
    signal_zero = signal_for_test()

    #assert on Empty
    assert collection._need_to_remove_head(signal_zero) == False

    collection.signal_list.append(signal_zero)

    #assert not too big and not too old
    assert collection._need_to_remove_head(signal_zero) == False

    collection.reset()


