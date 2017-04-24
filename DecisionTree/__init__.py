#/usr/bin/python3

# creates a decision tree based on training data
# uses the ID3 algorithm with maximum gain
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
        numPoints = len(data)                   # number of (training) data points

        # array of empty dictionaries
        counts = [{} for i in range(self._numAttributes)]

        # populate counts of each value seen
        # use these to calculate probabilities later
        for v in data:                          # iterate over each vector
            for i in range (self._numAttributes):
                val = v[i]
                if not val in counts[i]:
                    counts[i][val] = 0
                counts[i][val] += 1

        print(counts)


    # get probability of a specified attrbute having a given value
    def _getProportion(self, attr, val):
        if not val in counts[attr]:
            return 0.0
        return counts[attr][val] / self._numAttributes;


    # classify a vector (after training has been completed)
    def classify(self, x):
        pass
