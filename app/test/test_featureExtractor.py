# -*- coding: utf-8 -*-

"""Tests for signal collection """

import pytest

from classifier import featureExtractor

#Basic points
pointA = [2.0,4.0]
pointB = [1.0,2.0]

def test_center_of_line():
    """Simple center of line test"""
    assert featureExtractor.center_of_line(pointA, pointB) == (1.5, 3.0)

def test_length_of_line():
    """Simple length of line test"""
    assert featureExtractor.length_of_line(pointA, pointB) == 2.23606797749979

#Class for mocking signal
class Signal_test:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_x(self): 
        return self.x
    
    def get_y(self):
        return self.y

signalA = Signal_test(1.0, 1.0)
signalB = Signal_test(2.0, 2.0)
signal_list_test = [signalA, signalB]

def test_calculate_border_points():
    """Test the border point of signal test list"""
    assert featureExtractor.calculate_border_points(signal_list_test) == (1.0,1.0,2.0,2.0)

def test_calculate_center_of_mass_and_length():
    """Test for calculate center of mass and length"""
    assert featureExtractor.calculate_center_of_mass_and_length(signal_list_test) == ((1.5, 1.5), 1.4142135623730951)#TODO: check with data

def test_ratio_point_of_line():
    """Test for ratio point of line function"""
    assert featureExtractor.ratio_point_of_line(pointA, pointB, 0.5) == (1.5, 3.0)


