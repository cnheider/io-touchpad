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
from classifier import classifier as classifier_module

MIN_TRAINING_SIZE = 5

RUN_SUBCOMMAND = 'run'
RUN_USER_MODE = 'user'
RUN_32_MODE = '32'
RUN_64_MODE = '64'
ADD_SUBCOMMAND = 'add'
ACTIVATE_SUBCOMMAND = 'activate'
DELETE_SUBCOMMAND = 'delete'
DEACTIVATE_SUBCOMMAND = 'deactivate'
REPEAT_SUBCOMMAND = 'repeat'


def _get_configured_parser():
    """Configure the commandline arguments parser."""
    description = 'Teaching your touchpad magic tricks since 2016.'
    parser = argparse.ArgumentParser(add_help=True, description=description)

    subparsers = parser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand',
                                       help='available subcommands; run '
                                       'SUBCOMMAND -h to show help for '
                                       'the SUBCOMMAND you are interested in')
    subparsers.required = True  # Require SUBCOMMAND to be specified.

    # run.
    parser_run = subparsers.add_parser(RUN_SUBCOMMAND, help='run the app '
                                       'using hardcoded or user-defined '
                                       'symbols')
    parser_run.add_argument(dest='run_mode', metavar='MODE',
                            choices={RUN_32_MODE, RUN_64_MODE, RUN_USER_MODE},
                            help='set the mode you would like to run the '
                            'app in; use <32> for 32-bit machines, <64> for '
                            '64-bit machines and <user> to use user-defined '
                            'symbols')

    # activate.
    parser_activate = subparsers.add_parser(ACTIVATE_SUBCOMMAND,
                                            help='activate an existing '
                                            'symbol; the app will detect this '
                                            'symbol if the user draws it')
    parser_activate.add_argument(dest='symbol_name', default=None,
                                 metavar='SYMBOL', help='the name of the '
                                 'symbol the user wants to activate')

    # add.
    parser_add = subparsers.add_parser(ADD_SUBCOMMAND, help='undertake a '
                                       'learning session in order to add '
                                       'a new symbol')
    parser_add.add_argument(dest='training_size', default=None,
                            metavar='SIZE', help='you will be asked to draw '
                            'a symbol SIZE times; SIZE should be at '
                            'least ' + str(MIN_TRAINING_SIZE), type=int)
    parser_add.add_argument(dest='symbol_name', default=None,
                            metavar='SYMBOL', help='the name of the symbol '
                            'you want the app to learn during the learning '
                            'session')

    # deactivate.
    parser_deactivate = subparsers.add_parser(DEACTIVATE_SUBCOMMAND,
                                              help='deactivate an existing '
                                              'symbol; the app will not '
                                              'recognise this symbol; it will '
                                              'be possible to activate the '
                                              'symbol back later')
    parser_deactivate.add_argument(dest='symbol_name', default=None,
                            metavar='SYMBOL', help='the name of the symbol '
                            'the user wants to deactivate')

    # delete.
    parser_delete = subparsers.add_parser(DELETE_SUBCOMMAND, help='delete an '
                                          'existing symbol')
    parser_delete.add_argument(dest='symbol_name', default=None,
                               metavar='SYMBOL', help='the name of the symbol '
                               'you want to delete from the app')


    # repeat.
    parser_repeat = subparsers.add_parser(REPEAT_SUBCOMMAND, help='repeat the '
                                          'classification process of all '
                                          'symbols; use the --symbol option '
                                          'to repeat the process for only one '
                                          'symbol')
    parser_repeat.add_argument('-s', '--symbol', dest='symbol_name',
                               default=None, metavar='SYMBOL', help='the name '
                               'of the symbol on which you want to repeat the '
                               'classification process')

    return parser


def main():
    """The main function."""
    # SIGINT signal handler.
    terminationhandler.setup()

    parser = _get_configured_parser()
    args = parser.parse_args()

    training_size = None
    system_bitness = None
    learning_mode = None
    symbol_name = None

    if args.subcommand == REPEAT_SUBCOMMAND:
        print('Repeating the classification within the learning process.')
        classifier = classifier_module.Classifier(True)
        classifier.learn(True, args.symbol_name)
        sys.exit(0)

    if args.subcommand == ACTIVATE_SUBCOMMAND:
        print('app.py: warning: The command line argument "activate SYMBOL" '
              'has not been implemented yet.', file=sys.stderr)
        sys.exit(0)

    if args.subcommand == ADD_SUBCOMMAND:
        print('The symbol name is ' + args.symbol_name + '.')
        training_size = args.training_size
        if training_size < MIN_TRAINING_SIZE:
            print('app.py: error: the training size should be at least %d'
                  % (MIN_TRAINING_SIZE), file=sys.stderr)
            sys.exit(1)
        symbol_name = args.symbol_name
        learning_mode = True

    if args.subcommand == DEACTIVATE_SUBCOMMAND:
        print('app.py: warning: The command line argument "deactivate SYMBOL" '
              'has not been implemented yet.', file=sys.stderr)
        sys.exit(0)

    if args.subcommand == DELETE_SUBCOMMAND:
        print('app.py: warning: The command line argument "delete SYMBOL" '
              'has not been implemented yet.', file=sys.stderr)
        sys.exit(0)

    if args.subcommand == RUN_SUBCOMMAND:
        if args.run_mode != RUN_USER_MODE:
            system_bitness = int(args.run_mode)

    thread_queue = queue.Queue()

    # Run both threads.
    listener.start(thread_queue)
    application.application_thread(thread_queue, learning_mode, training_size,
                                   system_bitness, symbol_name)

main()
