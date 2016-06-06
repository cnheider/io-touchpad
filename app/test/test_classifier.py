# -*- coding: utf-8 -*-

"""Tests for classifier"""

import pytest
import operator
import filecmp
import difflib
import pickle
import sys
import shutil
from math import fabs

from classifier import classifier as classifier_module


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

epsilon = 0.00001

TEST_LOCATION = 'classifier/data/user-defined/'
PRE_TEST_FOLDER = 'pre_test/'


def setup_function(test_function):
    """Copy file with prepared data for test."""
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'symbol-list.dat',
                 TEST_LOCATION + 'symbol-list.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'nn-model.dat',
                 TEST_LOCATION + 'nn-model.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'nn-model_test.dat',
                 TEST_LOCATION + 'nn-model_test.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'nn-model_test2.dat',
                 TEST_LOCATION + 'nn-model_test2.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'distance-tolerance_test.dat',
                 TEST_LOCATION + 'distance-tolerance_test.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'distance-tolerance_test2.dat',
                 TEST_LOCATION + 'distance-tolerance_test2.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'training-set_test.dat',
                 TEST_LOCATION + 'training-set_test.dat')
    shutil.copy2(TEST_LOCATION + PRE_TEST_FOLDER + 'training-set_test2.dat',
                 TEST_LOCATION + 'training-set_test2.dat')


def test_reset_training_set():
    """Test for load training set."""
    classifier = classifier_module.Classifier(True, None)
    classifier.reset_training_set(117, "a")
    assert classifier.training_set == []
    assert classifier.training_size == 0
    assert classifier.ultimate_training_size == 117


def test_compute_tolerance_distance():
    """Test for computing distance.
    We put some list of list of features to calculate
    fixed distance, and check if it's same.
    """
    classifier = classifier_module.Classifier(True, None)
    L1 = [11.2, 41.43, 1.33]
    L2 = [10.9, 41.45, 1.34]
    L3 = [12.0, 41.4412, 1.001]
    L4 = [11.3, 41.15, 1.12]
    L5 = [11.223, 41.0, 1.31]
    AL = [L1, L2, L3, L4, L5]
    symbol = "a"
    classifier.compute_tolerance_distance(AL, symbol)
    tolerance_distance_path = \
        classifier_module.Classifier._get_file_path( \
            classifier.files[classifier_module.DISTANCE_TOLERANCE_FILE], symbol)
    file_with_tolerance_distance = \
        open(tolerance_distance_path, 'r')
    tolerance_distance = float(file_with_tolerance_distance.readline())
    file_with_tolerance_distance.close()
    assert fabs(tolerance_distance - 0.5506099238118276) < epsilon


def test__build_paths():
    """Test of the method which build file paths."""
    files1 = ["file1", "file2"]
    userdefined_path = classifier_module.DATA_PATH + classifier_module.USER_DIR

    expected_out_files1 = [operator.add(userdefined_path, file)
                           for file in files1]
    out_files1 = classifier_module.Classifier._build_paths(files=files1,
                                                           system_bitness=None)

    assert len(out_files1) == len(expected_out_files1)

    for file_num in range(len(out_files1)):
        assert out_files1[file_num] == expected_out_files1[file_num]


def test__extend_paths():
    """Test of the tiny helper function which expands a list of strings with a string."""
    file_paths = ["docs/abcd/", "docs/123/"]

    extend_paths = classifier_module.Classifier._extend_paths
    path_element = "u/"
    extended_paths = extend_paths(file_paths, path_element)

    assert len(file_paths) == len(extended_paths)
    for path_num in range(len(file_paths)):
        assert file_paths[path_num] + path_element == extended_paths[path_num]


def test_add_to_training_set():
    """Test if added list of points is in the set"""
    classifier = classifier_module.Classifier(True, None)
    classifier.add_to_training_set(SIGNAL_LIST_TEST)

    training_size = classifier.training_size
    added_list = classifier.training_set[training_size - 1]

    for i in range(0, len(SIGNAL_LIST_TEST) - 1):
        assert SIGNAL_LIST_TEST[i].get_x() == added_list[i].get_x()
        assert SIGNAL_LIST_TEST[i].get_y() == added_list[i].get_y()


def test_save_training_set():
    """Test learning symbol given the specific training set"""

    classifier = classifier_module.Classifier(True, None)
    classifier.delete_symbol('test')
    classifier.reset_training_set(7, 'test')
    for i in range(0, 5):
        signal_a = Signal_test(1.0 + i * 0.028, 1.00 - i * i * 0.20 * 0.30)
        signal_b = Signal_test(2.0 - i * 0.011, 2.00 - i * 0.020)
        signal_list_test = [signal_a, signal_b]

        classifier.add_to_training_set(signal_list_test)

    classifier.save_training_set("test")
    assert filecmp.cmp(TEST_LOCATION + 'symbol-list.dat',
                       TEST_LOCATION + 'expected_symbol-list.dat')
    assert filecmp.cmp(TEST_LOCATION + 'training-set_test.dat',
                       TEST_LOCATION + 'expected_training-set_test.dat') or \
           filecmp.cmp(TEST_LOCATION + 'training-set_test.dat',
                       TEST_LOCATION + 'expected2_training-set_test.dat')



def test_load_training_set():
    """Test loading training set from file"""
    classifier = classifier_module.Classifier(True, None)
    set = classifier.load_training_set('test')
    for i in range(0, 5):
        signal_list = set[i]
        assert signal_list[0].get_x() == 1.0 + i * 0.028
        assert signal_list[0].get_y() == 1.00 - i * i * 0.20 * 0.30

        assert signal_list[1].get_x() == 2.0 - i * 0.011
        assert signal_list[1].get_y() == 2.00 - i * 0.020



def test_learn_one_symbol():
    """Test learning specific symbol"""
    classifier = classifier_module.Classifier(True, None)
    tolerance = classifier.learn_one_symbol('test')

    file_with_model = open(TEST_LOCATION + 'test_nn_model.dat', 'rb')
    nbrs_from_file = pickle.load(file_with_model)

    assert 'ball_tree' == nbrs_from_file.algorithm
    assert 30 == nbrs_from_file.leaf_size
    assert 'minkowski' == nbrs_from_file.metric
    assert nbrs_from_file.metric_params is None
    assert 2 == nbrs_from_file.n_neighbors
    assert 2 == nbrs_from_file.p
    assert 1.0 == nbrs_from_file.radius
    assert tolerance < 398.85960989443032 + epsilon
    assert tolerance > 398.85960989443032 - epsilon


def test_classify():
    """Test classifying the given list of points to a symbol"""
    classifier = classifier_module.Classifier(False, None)
    for i in range(0, 5):
        signal_a = Signal_test(1.0 + i * 0.028, 1.00 - i * i * 0.20 * 0.30)
        signal_b = Signal_test(2.0 - i * 0.011, 2.00 - i * 0.020)
        signal_list_test = [signal_a, signal_b]

        symbol = classifier.classify(signal_list_test)
        assert symbol == 'test'


def test_delete_symbol():
    """Test deleting one symbol"""
    classifier = classifier_module.Classifier(True, None)
    classifier.symbol_list.append("test2")
    classifier.save_symbol_list()
    classifier.delete_symbol('test2')
    classifier.symbol_list.append("test3")
    classifier.save_symbol_list()


    assert filecmp.cmp(TEST_LOCATION + 'symbol-list.dat',
                       TEST_LOCATION + 'expected_test_delete_symbol.dat')


def test_delete_symbols():
    """Test deleting all symbols"""
    classifier = classifier_module.Classifier(True, None)

    classifier.save_training_set("test2")
    classifier.save_training_set("test3")
    classifier.save_training_set("test4")

    symbols_list = ['test2', 'test3', 'test4']
    classifier.delete_symbols(symbols_list)

    classifier.symbol_list.append("test2")
    classifier.save_symbol_list()

    assert filecmp.cmp(TEST_LOCATION + 'symbol-list.dat',
                       TEST_LOCATION + 'expected_test_delete_symbols.dat')