'''
Project 4: K-means Classificiation
Author: Dan Engbert
Date: 5-9-17

Implements a K-means classifier on the Iris dataset
'''
from Kmeans import Kmeans


"""Train a k-means classifier with the given data and labels."""
def train(data, labels, k=3):
    model = Kmeans()
    model.train(data, labels, k)
    return model


"""Classify a sample using the given model."""
def classify(x, model):
    res = model.classify(x)
    return res
