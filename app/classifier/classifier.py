# -*- coding: utf-8 -*-
"""Classifier class."""

import _thread
import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
import sys
import math
from classifier import featureExtractor

DATA_PATH = 'classifier/data/'
DISTANCE_TOLERANCE_FILE = DATA_PATH + 'distance-tolerance.dat'
MODEL_FILE = DATA_PATH + 'nn-model.dat'
TRAINING_SET_FILE = DATA_PATH + 'training-set.dat'


class Classifier:

    """Class for learning and classifying drawn symbols."""

    def __init__(self, learning_mode=False):
        """Constructor. Loads learning model from file."""
        if not learning_mode:

            try:
                file_with_model = open(MODEL_FILE, 'rb')
            except FileNotFoundError:
                print("File with learning-model doesn't exist, please do learning.")
                _thread.interrupt_main()
                sys.exit(1)

            self.learning_model = pickle.load(file_with_model)
            file_with_model.close()

            try:
                file_with_tolerance_distance = open(DISTANCE_TOLERANCE_FILE, 'r')
            except FileNotFoundError:
                print("File with tolerance distance doesn't exist, please do learning.")
                _thread.interrupt_main()
                sys.exit(1)

            self.tolerance_distance = \
                float(file_with_tolerance_distance.readline())
            file_with_tolerance_distance.close()

        # variables for learning-mode
        self.training_size = 0
        self.ultimate_training_size = 0
        self.training_set = []

    def load_training_set(self):
        """Load traning symbols from file."""
        try:
            file_with_training = open(TRAINING_SET_FILE, 'rb')
        except FileNotFoundError:
            print("File with training-set doesn't exist, please do learning.")
            _thread.interrupt_main()
            sys.exit(1)

        training_set = pickle.load(file_with_training)
        file_with_training.close()
        return training_set

    def reset_training_set(self, new_training_size):
        """Start the new training set."""
        self.ultimate_training_size = new_training_size
        self.training_size = 0
        self.training_set = []

    def add_to_training_set(self, signal_list):
        """Add the symbol to training set."""
        print("training...")
        self.training_set.append(signal_list)
        self.training_size += 1
        print("ok")
        if self.training_size == self.ultimate_training_size:
            self.learn(False)
            _thread.interrupt_main()
            sys.exit(0)
        print()

    def classify(self, signal_list):
        """Classify the symbol to some item id or return None if similirity is to weak."""
        print("classifing...")
        feature_vector = featureExtractor.get_features(signal_list)
        distances, _ = self.learning_model.kneighbors(np.array([feature_vector]))
        mean_distance = np.mean(distances[0])
        print(mean_distance)
        if mean_distance < self.tolerance_distance:
            return 1
        else:
            return None

    def compute_tolerance_distance(self, sample):
        """Compute the distance in the feature vectors space below which we find the symbol similar."""
        nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(sample)
        distances, _ = nbrs.kneighbors(sample)
        print(distances)
        means = []
        for distances_row in distances:
            row = np.delete(distances_row, [0])
            means.append(np.mean(row))
        means.sort()
        critical_index = math.ceil(0.8 * len(means)) - 1
        self.tolerance_distance = means[critical_index] * 1.3
        print("tolerance distance: %.16f" % (self.tolerance_distance))
        file_with_tolerance_distance = open(DISTANCE_TOLERANCE_FILE, 'w')
        file_with_tolerance_distance.write("%.16f\n" % (self.tolerance_distance))
        file_with_tolerance_distance.close()

    def learn(self, load_from_file):
        """Load training symbols and learn."""
        print("learning...")
        if not load_from_file:
            file_with_training = open(TRAINING_SET_FILE, 'wb')
            pickle.dump(self.training_set, file_with_training)
            file_with_training.close()
        training_set = self.load_training_set()
        feature_vectors = []
        for training_element in training_set:
            feature_vectors.append(featureExtractor.get_features(training_element))
        sample = np.array(feature_vectors)
        nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(sample)
        file_with_model = open(MODEL_FILE, 'wb')
        pickle.dump(nbrs, file_with_model)
        file_with_model.close()
        self.compute_tolerance_distance(sample)
