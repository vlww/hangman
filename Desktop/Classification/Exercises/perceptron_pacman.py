# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# ----------


# Perceptron implementation for imitation learning
import Helpers.util
from Exercises.perceptron_multiclass import PerceptronClassifier
from random import uniform
from pacman import GameState


class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, maxIterations)
        self.epochs = maxIterations
        self.weights = [] 
        

    def convert_data(self, data):
        # fix datatype issues
        # if it comes in inside of a list, pull it out of the list
        if isinstance(data, list):
            data = data[0]

        #data comes as a tuple
        all_moves_features = data[0] #grab the features (dict of action->features)
        legal_moves = data[1]        #grab the list of legal moves from this state
        return_features = {}
        #loop each action
        for key in all_moves_features:
            #convert feature values from dict to list
            all_features = ['foodCount', 'STOP', 'nearest_ghost', 'ghost-0', 'capsule-0', 'food-0', 'food-1', \
                            'food-2', 'food-3', 'food-4', 'capsule count', 'win', 'lose', 'score']
            dict_features = all_moves_features[key] 
            list_features = []
            # grab all feature values & put them in a list
            for feat in all_features:
                if feat not in dict_features:
                    list_features.append(0)
                else:
                    list_features.append(dict_features[feat])
            return_features[key] = list_features

        return (return_features, legal_moves) 


    def classify(self, data):
        #leave this call to convert_data here!
        features, legal_moves = self.convert_data(data)

        ##your code goes here##
        max_sum = float('-inf')
        highest_index = 0
        weight_index = 0
        for l in legal_moves:
            sum = 0
            for c in range(len(features[l])):
                sum += features[l][c]*self.weights[c]
            if sum > max_sum:
                max_sum = sum
                highest_index = weight_index
            weight_index += 1

        #your predicted_label needs to be returned inside of a list for the PacMan game
        predicted_label = 'Stop'
        return [legal_moves[highest_index]]


    def train(self, train_data, labels):
        for i in range(14):
            self.weights.append(uniform(-1, 1))
        for epoch in range(self.epochs):
            for r in range(len(train_data)):
                features, legal_moves = self.convert_data(train_data[r])
                predicted = self.classify(train_data[r])[0]
                actual = labels[r]
                actfeatures = features[actual]
                predfeatures = features[predicted]
                if actual != predicted:
                    for w in range(len(self.weights)):
                        self.weights[w] += actfeatures[w]
                        self.weights[w] -= predfeatures[w]
