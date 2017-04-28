import math
from DecisionTree import Tree
from copy import deepcopy


# creates a decision tree based on training data
# uses the ID3 algorithm with maximum gain
class DecisionTree:

    # generate the decision tree based on the provided training data
    # data must be an array of integer arrays (each of the same length)
    # labels must be an array of integers
    # len(data) must == len(labels)
    def train(self, data, labels):
        self._data = data
        self._labels = labels
        numAttributes = len(data[0])            # should be same across all data points

        pAttr = list(range(numAttributes))      # list of attributes to possibly split on
        rlist = list(range(len(data)))          # initially all points are remaining in the data set
        self._root = Tree.Tree()
        self._createTree(self._root, pAttr, rlist)
        # no longer need to remember the training data
        self._data = []
        self._labels = []


    # recursively generates the decision tree based on maximum gain
    # pAttr: array of possible attributes to split on
    # rlist: indices (in data/labels) of data points in the remaining data subset
    def _createTree(self, tree, pAttr, rlist):
        # check if all members of subset are classified the same
        first_label = self._labels[rlist[0]]
        for r in range(1, len(rlist)):
            i = rlist[r]                        # relevant index of a data point
            lbl = self._labels[i]
            if lbl != first_label:
                break
            if r == (len(rlist) - 1):
                tree.final_label = first_label
                return

        # when there are no attributes left to split on
        if len(pAttr) == 0:
            tree.chooseBest(self._getLabelCount(rlist))
            return

        gains = [0 for i in range(len(pAttr))]
        for i in range(len(pAttr)):             # iterate over attribute array
            a = pAttr[i]                        # current attribute
            gains[i] = self._gain(a, rlist)

        maxGain = 0                             # index of max gain
        for i in range(len(gains)):
            if gains[i] > gains[maxGain]:
                maxGain = i

        # if all gains are 0 stop branching and use the most popular label
        # (in some data sets there may be duplicate vectors with different classifications)
        if gains[maxGain] == 0:
            tree.chooseBest(self._getLabelCount(rlist))
            return

        tree.attr = pAttr[maxGain]              # attribute to split on
        del pAttr[maxGain]                      # remove attribute we're using from list

        vals_dist = self._valDistribution(tree.attr, rlist)

        # possible (remaining) vals for this attribute to take on
        tree.vals = list(vals_dist)
        tree.subTrees = [Tree.Tree() for i in range(len(tree.vals))]

        # iterate over each value to branch off of
        # recursively create tree for each possible value taken on by the attribute
        # use deep copies of pAttr!
        for i in range(len(tree.vals)):
            self._createTree(tree.subTrees[i], deepcopy(pAttr), vals_dist[tree.vals[i]])


    # information gain for a specific attribute
    def _gain(self, a, rlist):
        return self._entropy(rlist) + self._expectedEntropy(a, rlist)


    # returns the entropy of a subset of the data
    # rlist is a list of the indices in data/label that are make up the subset
    def _entropy(self, rlist):
        labels = self._labels
        total = 0.0
        label_count = self._getLabelCount(rlist)

        for lbl in label_count:
            p = self._getLabelProportion(lbl, label_count, len(rlist))
            total += -1 * p * math.log(p, 2)
        return total


    # epected entropy after splitting on attribute number a
    def _expectedEntropy(self, a, rlist):
        total = 0.0
        vals = self._valDistribution(a, rlist)

        # iterate over each subset
        for val in vals:
            # subset of the (remaining) data such that every element has value val for attribute a
            sub = vals[val]
            s_v = len(sub)
            sub_entropy = self._entropy(sub)
            total += -1 * s_v / len(rlist) * sub_entropy

        return total


    def _valDistribution(self, a, rlist):
        # list of subsets split on each value of the attribute
        # a subset is represented as a list of relevant indices in data/labels
        vals = {}

        for i in rlist:
            # i is the relevant index of a data point
            p = self._data[i]                   # current data point (vector)
            val = p[a]
            if not val in vals:
                vals[val] = []
            vals[val].append(i)
        return vals


    # create count of label distribution across remaining data points
    def _getLabelCount(self, rlist):
        label_count = {}
        # count number of occurences of each label value
        for i in rlist:
            lbl = self._labels[i]               # label of relevant data point
            if not lbl in label_count:
                label_count[lbl] = 0
            label_count[lbl] += 1

        return label_count


    # get ratio of (remaining) data points with this label
    def _getLabelProportion(self, lbl, label_count, numPoints):
        if not lbl in label_count:
            return 0.0
        return label_count[lbl] / numPoints;


    # classify a vector (after training has been completed)
    def classify(self, x):
        tree = self._root
        while True:
            if tree.final_label != None:
                return tree.final_label

            x_val = x[tree.attr]
            tree = tree.getRelevantSubtree(x_val)
