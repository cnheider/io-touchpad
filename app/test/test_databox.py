# -*- coding: utf-8 -*-

"""Tests for touchpad signal """

import pytest

from databox import databox

command = databox.Command("echo","ok")

# Test section

def test_get_command_and_argument():
    comm, argument = command.get_command_and_argument()
    
    assert comm == "echo"
    assert argument == "ok"

def test_is_user_defined():
    assert command.is_user_defined('not_in') == False

def test_is_builtin():
    assert command.is_builtin('1') == True
    assert command.is_builtin('not_in') == False

def test_get_command_and_arguments():
    assert databox.get_command_and_arguments('not_in') == None

    comm, argument = databox.get_command_and_arguments('1')
    
    assert comm == 'x-www-browser'
    assert argument == ''
