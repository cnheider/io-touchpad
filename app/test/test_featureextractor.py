# -*- coding: utf-8 -*-

"""Tests for signal collection."""

import pytest

from classifier import featureextractor
from math import pi

# Basic points
POINTA = featureextractor.Point(2.0, 4.0)
POINTB = featureextractor.Point(1.0, 2.0)


def test_flip_horizontally():
    """Simple flip vertically test.

    """
    point = featureextractor.Point(5, 3)
    expected = featureextractor.Point(-5, 3)
    point.flip_horizontally()

    assert point.equals(expected)


def test_flip_vertically():
    """Simple flip vertically test.

    """
    point = featureextractor.Point(5, 3)
    expected = featureextractor.Point(5, -3)
    point.flip_vertically()

    assert point.equals(expected)


def test_center_of_line():
    """Simple center of line test.

    """
    line = featureextractor.Line(POINTA, POINTB)
    expected = featureextractor.Point(1.5, 3)
    assert line.center_point().equals(expected)


def test_ratio_point():
    """Test for ratio point of line function.

    """
    line = featureextractor.Line(POINTA, POINTB)
    expected = featureextractor.Point(1.25, 2.50)
    assert line.ratio_point(0.75).equals(expected)


def test_length_of_line():
    """Simple length of line test.

    """
    line = featureextractor.Line(POINTA, POINTB)
    expected = 2.23606797749979

    assert line.length() == expected


# Tests for Scaler
def test_move_point():
    """Test move point function.

    """

    min_point = featureextractor.Point(0.0, 0.0)
    max_point = featureextractor.Point(5.0, 7.0)
    scaler = featureextractor.Scaler(min_point, max_point, POINTB)

    assert scaler.move_point(POINTA).x_cord == POINTB.x_cord
    assert scaler.move_point(POINTA).y_cord == POINTB.y_cord


def test_scale_point():
    """Test scaling point function.

    """
    min_point = featureextractor.Point(0.0, 0.0)
    max_point = featureextractor.Point(5.0, 7.0)
    scaler = featureextractor.Scaler(min_point, max_point, POINTB)

    expected = featureextractor.Point(142.85714285714286, 285.7142857142857)
    assert scaler.scale_point(POINTA).x_cord == expected.x_cord
    assert scaler.scale_point(POINTA).y_cord == expected.y_cord


# Tests for Curve class
def test_actualise_center_of_mass():
    """Test actualisation of center of mass in class Curve

    """
    origin = featureextractor.Point(0.0, 0.0)

    curve = featureextractor.Curve(origin)
    curve.length = 6
    curve.actualise_center_of_mass(featureextractor.Point(2.5, 0.0), 5)

    assert curve.center_of_mass.equals(featureextractor.Point(12.5/11.0, 0))


def test_add_point():
    """Test adding point to the curve.

    """
    curve = featureextractor.Curve(featureextractor.Point(0.0, 0.0))
    length = 0.0
    for x in range(1, 10):
        curve.add_point(featureextractor.Point(3*x, 4*x))
        length += 5
        assert curve.center_of_mass.equals(featureextractor.Point(1.5*x, 2*x))
        assert curve.length == length


# Class for mocking signal
class Signal_test:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self): 
        return self.x

    def get_y(self):
        return self.y

    def is_proper_signal_of_point(self):
        return True

    def is_raising_finger_signal(self):
        return False

SIGNALA = Signal_test(1.0, 1.0)
SIGNALB = Signal_test(2.0, 2.0)
SIGNAL_LIST_TEST = [SIGNALA, SIGNALB]


def test_calculate_border_points():
    """Test the border point of signal test list.

    """
    expected1 = featureextractor.Point(1.0, 1.0)
    expected2 = featureextractor.Point(2.0, 2.0)

    point1, point2 = featureextractor.calculate_border_points(SIGNAL_LIST_TEST)
    assert point1.equals(expected1)
    assert point2.equals(expected2)


def test_angle_between_line_and_xaxis():
    """Test for angle between line and xaxis.

    """
    PA = featureextractor.Point(2, 2)
    PB = featureextractor.Point(-6, -6)
    assert featureextractor.angle_between_line_and_xaxis(PA, PB) == pi/4


def test_join_features():
    """Test for joining features.

    """
    P1 = featureextractor.Point(3, 4)
    P2 = featureextractor.Point(5, 6)
    P3 = featureextractor.Point(7, 8)
    PLIST = [P1, P2, P3]
    F1 = [3.3, 2.2]
    C1 = [5.6, 45, 12]

    assert len(featureextractor.join_features(PLIST, F1, C1)) == 11


def test_create_normalized_curve():
    """Test for creating 40 equidistant points

    """
    curve = featureextractor.Curve(featureextractor.Point(0, 0))
    x = 0

    colors = [0]

    last_point = featureextractor.Point(0, 0)
    for i in range(1, 42):
        x += i
        point = featureextractor.Point(x*x, 0)
        curve.add_point(point)
        colors.append(0)
        last_point = point
    start_point = featureextractor.Point(0, 0)
    normalized = featureextractor.\
        create_normalized_curve(curve, start_point, last_point, colors)
    expected_x = -500.0
    for point in normalized.list_of_points:

        assert point.x_cord < expected_x + 0.000001
        assert point.x_cord > expected_x - 0.000001
        expected_x += 1000.0/39.0


def test_get_angle_list():
    """Test for checking angles in Curve

    """

    curve = featureextractor.Curve(featureextractor.Point(0, 0))

    colors = [0]
    SCALING = 2 / pi * \
              (featureextractor.SCALE / featureextractor.ANGLE_DOWNSCALE)
    for x in range(1, 42):
        point = featureextractor.Point(x, x*x)
        curve.add_point(point)
        colors.append(0)

    angles = featureextractor.get_angle_list(curve)
    for i in range(0, featureextractor.NUMBER_OF_POINTS - 2):
        angle = angles[i]
        point1 = curve.list_of_points[i]
        point2 = curve.list_of_points[i + 1]
        expected_angle = featureextractor.\
            angle_between_line_and_xaxis(point1, point2)
        expected_angle *= SCALING

        assert angle < expected_angle + 0.000001
        assert angle > expected_angle - 0.000001


def test_filter_points_from_signal_and_normalize_curve():
    signals = []
    exp_points = []
    for i in range(0, 100):
        signals.append(Signal_test(i, 8*i + 2))
        exp_points.append(featureextractor.Point(i, 8*i + 2))

    points, colors = featureextractor.filter_points_from_signals(signals)

    for i in range(0, 100):
        assert points[i].x == exp_points[i].x_cord
        assert points[i].y == exp_points[i].y_cord
        assert colors[i] == 0

    curve = featureextractor.normalize_points(points, colors)

    for i in range(0, featureextractor.NUMBER_OF_POINTS - 1):
        point = curve.list_of_points[i]
        x_jump = 2.5 + 0.705128205128055
        x = -62.5 + i * x_jump
        y = i * 1000.0 / (featureextractor.NUMBER_OF_POINTS - 1)
        assert point.x_cord < x + 0.00001
        assert point.x_cord > x - 0.00001

        assert point.y_cord < -500 + y + 0.00001
        assert point.y_cord > -500 + y - 0.00001


def test_feature_extractor():
    """Test for  extracted features.

    """
    signal_list = []
    for i in range(0, 20):
        signal_list.append(Signal_test(i, i))

    features = featureextractor.get_features(signal_list)
    minimum = 0
    maximum = 0
    for feature in features:
        print(feature)
        if feature < minimum:
            minimum = feature
        if feature > maximum:
            maximum = feature

    assert minimum > -500.0 - 0.000001
    assert minimum < -500.0 + 0.000001
    assert maximum < 500.0 + 0.000001
    assert maximum > 500.0 - 0.000001
