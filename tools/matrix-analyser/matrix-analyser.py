#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

class Touchpad:
    def __init__(self, touchpad, tolerance):
        # Enter your laptop here.
        if 'haseeq540s' == touchpad:
            self.initialize(1472, 5472, 1408, 4448, tolerance)

    def initialize(self, min_x, max_x, min_y, max_y, tolerance):
        self.min_x = min_x
        self.max_x = max_x + tolerance
        self.min_y = min_y
        self.max_y = max_y + tolerance
        self.x_range = max_x - min_x
        self.y_range = max_y - min_y


def main():
    touchpad = Touchpad('haseeq540s', 300)
    X = []
    Y = []

    with open('data/coordinates.data') as file:
        for line in file:
            vector = line.split()
            X.append(int(vector[0]) - touchpad.min_x)
            Y.append(int(vector[1]) - touchpad.min_y)

    print("x range: %d, y range: %d" % (touchpad.x_range, touchpad.y_range))

    plt.gca().invert_yaxis()
    plt.scatter(X, Y, s=3)
    plt.savefig('figures/matrix.png', dpi=500)
    plt.show()

main()
