# -*- coding: utf-8 -*-

"""Tests for signal collection """

import pytest

from signalcollection import signalcollection


def test_reset():
    """Test for reseting signal list"""
    collection = signalcollection.SignalCollection()

    collection.signal_list = [5]
    assert collection.signal_list == [5]

    collection.reset()
    assert collection.signal_list == []

def test_init():
    """Test for initial function"""
    collection = signalcollection.SignalCollection()

    assert collection.signal_list == []
