# -*- coding: utf-8 -*-
"""Classifier class.
"""

class Classifier:

    training_size = 0
    ultimate_training_size = 0

    def __init__(self):
        pass
        #TODO load classifying model from file
    
    def reset_training_set(self, new_training_size):
        print("reset")
        print(new_training_size)
        self.ultimate_training_size = new_training_size
        self.training_size = 0
        #TODO cleaning files

    def add_to_training_set(self, signal_list):
        print("training...")
        print(signal_list)
        #TODO adding drawn symbol to history file, if enough training elements - call learn

    def calculate_feature_vector(self, signal_list):
        print("calculating features")
        pass

    def classify(self, signal_list):
        print("classyfing...")
        print(signal_list)
        feature_vector = self.calculate_feature_vector(signal_list)
        #TODO knn
    
    def learn(self):
        print("learn")
        #feature_vector = self.calculate_feature_vector(signal_list)
        #TODO load drawings from history, build and save knn model, compute "similarity distance" and save
