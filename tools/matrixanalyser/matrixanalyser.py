#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a utility to visualize the symbols drawn on touchpads.

It reads the data/coordinates.data file where every line is in the
"%d %d" % (x, y) format. Subsequently, it saves the generated
figure as a figures/matrix.png file and shows a window with
the figure.

You'll need matplotlib to make it work.
Sometimes matplotlib doesn't work when using virtual environment
like pyvenv. It is advised to download it using your system
package manager.

Important! Add the specification of your laptop's touchpad to the if
statement in the __init__ within the Touchpad class. You can find
out what is the resolution of your touchpad running evtest.
"""

import sys
import matplotlib.pyplot as plt

class Touchpad:
    """A class representing a touchpad.

    Attributes:
        min_x (int): Lower bound of the x-axis resolution.
        max_x (int): Upper bound of the x-axis resolution.
        min_y (int): Lower bound of the y-axis resolution.
        max_y (int): Upper bound of the y-axis resolution.
        x_range (int): x-axis range.
        y_range (int): y-axis range.

    """

    def __init__(self, touchpad, tolerance=None):
        """
        Calls the initialize function with the parameters for the
        given touchpad.

        Args:
            param1 touchpad (str): The name of a laptop.
                It should be added in the if statement below.
            param2 tolerance (int): Sometimes the resolution of
                the touchpad is not exactly like the one suggested
                by evtest. This is why we have to add some space to
                avoid out of range errors.
        """
        if touchpad == 'haseeq540s':
            tolerance = tolerance if tolerance else 300
            self._initialize(1472, 5472, 1408, 4448, tolerance)
        else:
            print("You should change the laptop's model you are asking for." \
                    "Or specify a new one in the code on your own.")
            sys.exit(1)

    def _initialize(self, min_x, max_x, min_y, max_y, tolerance):
        """Initialize the Touchpad

        Args:
            min_x (int): Lower bound of the x-axis resolution.
            max_x (int): Upper bound of the x-axis resolution.
            min_y (int): Lower bound of the y-axis resolution.
            max_y (int): Upper bound of the y-axis resolution.
            tolerance (int): Additional range to avoid out of range
                errors.
        """
        self.min_x = min_x
        self.max_x = max_x + tolerance
        self.min_y = min_y
        self.max_y = max_y + tolerance
        self.x_range = max_x - min_x
        self.y_range = max_y - min_y


def usage():
    """Basic usage information.
    """
    print("Usage: ./matrixanalyzer <laptop model> [tolerance]")


def main():
    """The main function.
    """
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    touchpad_model = sys.argv[1]
    tolerance = sys.argv[2] if len(sys.argv) == 3 else None

    touchpad = Touchpad(touchpad_model, tolerance)
    x_coordinates = []
    y_coordinates = []

    with open('data/coordinates.data') as file:
        for line in file:
            vector = line.split()
            x_coordinates.append(int(vector[0]) - touchpad.min_x)
            y_coordinates.append(int(vector[1]) - touchpad.min_y)

    print("x range: %d, y range: %d" % (touchpad.x_range, touchpad.y_range))

    plt.gca().invert_yaxis()
    plt.scatter(x_coordinates, y_coordinates, s=3)
    plt.savefig('figures/matrix.png', dpi=500)
    plt.show()

main()
