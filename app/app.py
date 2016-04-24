#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""io-touchpad application.

This application will learn to associate symbols you draw on your touchpad
with certain actions you bound to those symbols.

Your finger's absolute position is fetched using a library called touchpadlib
which is based on evtest (version 1.32).

Source code encoding: UTF-8
"""

import argparse
import queue
import sys

from terminationhandler import terminationhandler
from threads import application
from threads import listener
from touchpadlib import touchpadlib
from classifier import classifier

MIN_TRAINING_SIZE = 3

def main():
    """The main function."""
    # SIGINT signal handler.
    terminationhandler.setup()

    description = 'Teaching your touchpad magic tricks since 2016.'
    parser = argparse.ArgumentParser(description=description)
    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument('-s', '--system', dest='system_bitness',
        default=None, metavar='BITS', help='set the bitness of your '
        'operation system; this option triggers the use of the hardcoded '
        'symbols', choices={'32', '64'})
    parser_group.add_argument('-l', '--learning', dest='training_size',
        default=None, metavar='SIZE', help='start the application in the '
        'learning mode; you will be asked to draw a symbol SIZE times; '
        'SIZE should be at least ' + str(MIN_TRAINING_SIZE), type=int)
    parser_group.add_argument('-r', '--repeat', dest='repeat_classification',
        default=False, action='store_true', help='repeat the classification '
        'on the latest user-defined set of drawings')
    args = parser.parse_args()

    if args.repeat_classification:
        print('Repeating the classification within the learning process.')
        clsf = classifier.Classifier()
        clsf.learn(True)
        sys.exit(0)

    training_size = args.training_size
    learning_mode = training_size is not None
    if learning_mode and training_size < 3:
        print('app.py: error: the training size should be at least %d'
            % (MIN_TRAINING_SIZE))
        sys.exit(1)

    thread_queue = queue.Queue()

    touchpad_specification = touchpadlib.Touchpadlib.get_specification()

    print("Touchpad specification: "
          "min/max x: %d/%d, min/max y: %d/%d, min/max pressure %d/%d." %
          (touchpad_specification['min_x'],
           touchpad_specification['max_x'],
           touchpad_specification['min_y'],
           touchpad_specification['max_y'],
           touchpad_specification['min_pressure'],
           touchpad_specification['max_pressure']))

    # Greating.
    if learning_mode:
        print("Welcome to learning mode.\n"
              "Think of a symbol you want the application to learn "
              "and draw it %d times." % (training_size))
    else:
        print("Use your touchpad as usual. Have a nice day!")

    # Run both threads.
    listener.start(thread_queue)
    application.application_thread(thread_queue, learning_mode, training_size)

main()
