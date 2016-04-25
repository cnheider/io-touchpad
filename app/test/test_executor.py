# -*- coding: utf-8 -*-

"""Tests for touchpad signal """

import pytest

from executor import executor

def test_execute():

    assert executor.execute(-1) == False

    assert executor.execute(0) == True
