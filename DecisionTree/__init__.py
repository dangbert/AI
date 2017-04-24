#/usr/bin/python3

class DecisionTree:

    # constructor
    def __init__(self):
        pass

    # generate the decision tree based on the provided training data
    # data must be an array of integer arrays (each of the same length)
    # labels must be an array of integers
    # len(data) must == len(labels)
    def train(self, data, labels):
        self._numAttributes = len(data[0])


    # classify a vector (after training has been completed)
    def classify(self, x):
        pass
