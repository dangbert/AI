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
        self.numPoints = len(data)              # number of (training) data points

        # array of empty dictionaries
        self._counts = [{} for i in range(self._numAttributes)]
        self._label_counts = {}                       # number of times each label is used

        for n in range(len(data)):              # iterate over each vector (data point)
            # count number of occurences of each label value
            if not labels[n] in self._label_counts:
                self._label_counts[labels[n]] = 0
            self._label_counts[labels[n]] += 1

            v = data[n]
            # for each attribute, count the number of times each value is seen
            for i in range (self._numAttributes):
                val = v[i]
                if not val in self._counts[i]:
                    self._counts[i][val] = 0
                self._counts[i][val] += 1

        print(self._counts)
        print(self._label_counts)


    # get probability of a specified attrbute having a given value
    def _getProportion(self, attr, val):
        if not val in self._counts[attr]:
            return 0.0
        return self._counts[attr][val] / self._numAttributes;


    # get proportion of a specific label value amongst all classifications
    def _getLabelProportion(self, label):
        if not label in self._label_counts:
            return 0.0
        return self._label_counts[label] / self._numPoints;


    # classify a vector (after training has been completed)
    def classify(self, x):
        pass
