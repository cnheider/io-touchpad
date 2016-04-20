# -*- coding: utf-8 -*-
"""Classifier class.
"""
import _thread
import pickle

class Classifier:

    training_size = 0
    ultimate_training_size = 0

    def __init__(self):
        print("init");
        #TODO load classifying model from file

    def load_training_set(self):
        self.file_with_sizes = open('drawings-sizes', 'r')
        self.file_with_signals = open('drawings-signals', 'rb')
        number_of_symbols = int(self.file_with_sizes.readline())
        print(number_of_symbols)
        training_set = []
        for i in range(0, number_of_symbols):
            symbol_size = int(self.file_with_sizes.readline())
            print(symbol_size)
            signals = []
            for j in range(0, symbol_size):
                touchpad_signal = pickle.load(self.file_with_signals)
                print(touchpad_signal)
                signals.append(touchpad_signal)
            training_set.append(signals)
        self.file_with_sizes.close()
        self.file_with_signals.close()
        return training_set

    def reset_training_set(self, new_training_size):
        print("reset")
        print(new_training_size)
        self.ultimate_training_size = new_training_size
        self.training_size = 0
        self.file_with_sizes = open('drawings-sizes', 'w')
        self.file_with_sizes.write("%d\n" % (new_training_size))
        self.file_with_signals = open('drawings-signals', 'wb')

    def add_to_training_set(self, signal_list):
        print("training...")
        print(len(signal_list))
        self.file_with_sizes.write("%d\n" % (len(signal_list)))
        for element in signal_list:
            pickle.dump(element, self.file_with_signals)
        self.training_size += 1
        if self.training_size == self.ultimate_training_size:
            self.file_with_sizes.close()
            self.file_with_signals.close()
            self.learn()
            _thread.interrupt_main()
            sys.exit(0)

    def calculate_feature_vector(self, signal_list):
        print("calculating features")
        #temporal stupid features:
        le = len(signal_list) % 5
        return [le,le+1,le+2,le+3]

    def classify(self, signal_list):
        print("classyfing...")
        print(len(signal_list))
        feature_vector = self.calculate_feature_vector(signal_list)
        #TODO knn
    
    def learn(self):
        print("learning...")
        training_set = self.load_training_set()
        print(training_set)
        #feature_vector = self.calculate_feature_vector(signal_list)
        #TODO load drawings from history, build and save knn model, compute "similarity distance" and save
