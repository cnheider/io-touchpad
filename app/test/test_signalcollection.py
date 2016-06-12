# -*- coding: utf-8 -*-

"""Tests for signal collection """

from signalcollection import signalcollection

COLLECTION = signalcollection.SignalCollection()


class TestSignal:

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time


def test_init():
    """Test for initial function"""
    assert COLLECTION.signal_list == []


def test_reset():
    """Test for reseting signal list"""
    COLLECTION.signal_list = [5]
    assert COLLECTION.signal_list == [5]

    COLLECTION.reset()
    assert COLLECTION.signal_list == []


def test__is_to_big():
    """Test _is_too_big function"""
    maxi = signalcollection.MAX_NUMBER_OF_SIGNALS_IN_GROUP

    for i in range(0, maxi - 1):
        COLLECTION.signal_list.append(i)

    assert COLLECTION._is_too_big() is False

    COLLECTION.signal_list.append(-1)

    assert COLLECTION._is_too_big() is True


def test__is_empty():
    """Test _is_empty function"""
    COLLECTION.signal_list = [5]
    assert COLLECTION._is_empty() is False

    COLLECTION.reset()
    assert COLLECTION._is_empty() is True


def test_as_list():
    """Test as_empty function"""
    assert COLLECTION.as_list() == COLLECTION.signal_list


def test_is_head_too_old():
    """Test is_head_too_old function"""

    # We put signal with time 0.
    signal_zero = TestSignal()
    signal_zero.set_time(0)

    COLLECTION.signal_list.append(signal_zero)

    signal_maxi = TestSignal()
    signal_maxi.set_time(signalcollection.MAX_DURATION_OF_GROUP)

    assert COLLECTION._is_head_too_old(signal_maxi) is False

    signal_maxi.set_time(signalcollection.MAX_DURATION_OF_GROUP+0.1)

    assert COLLECTION._is_head_too_old(signal_maxi) is True

    COLLECTION.reset()


def test_is_recent_enough():
    """Test is_recent_enough function."""

    # We put signal with time 0.
    signal_zero = TestSignal()
    signal_zero.set_time(0)

    COLLECTION.signal_list.append(signal_zero)
    assert COLLECTION.is_recent_enough(COLLECTION
                                       .get_max_break_between_two_points())\
        is True
    assert COLLECTION.is_recent_enough(COLLECTION
                                       .get_max_break_between_two_points() +
                                       0.1) is False

    COLLECTION.reset()


def test__need_to_remove_head():
    """Test need_to_remove_head function"""

    # We put signal with time 0.
    signal_zero = TestSignal()
    signal_zero.set_time(0)

    # assert on Empty
    assert COLLECTION._need_to_remove_head(signal_zero) is False

    COLLECTION.signal_list.append(signal_zero)

    # Assert not too big and not too old.
    assert COLLECTION._need_to_remove_head(signal_zero) is False

    COLLECTION.reset()
