#/usr/bin/python3
import math
from DecisionTree import Tree
from copy import deepcopy


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
        self._numPoints = len(data)              # number of (training) data points

        # array of empty dictionaries
        self._counts = [{} for i in range(self._numAttributes)]
        self._label_counts = {}                 # number of times each label is used

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

        #print("data=")
        #print(data)
        #print("labels=")
        #print(labels)
        #print("\n\n")
        print(self._counts)
        print(self._label_counts)
        # TODO: might not need label_counts
        # TODO: consider moving (some) of these functions to Tree class???

        # recursively generate the decision tree based on maximum gain
        # TODO: consider storing data, labels in the class so that it doesnt have to keep being
        # passed around. then delete them after training is done
        tree = Tree.Tree()
        # indicies of possible vector attributes to consider
        pAttr = list(range(self._numAttributes))
        rlist = list(range(len(data)))          # initially all points are remaining in the data set
        self._labels = labels
        self._data = data
        self._createTree(tree, pAttr, rlist)


    # modifies a tree
    # pAttr: array of possible attributes to split on
    # data is the remaining data that made it to this point in the decision tree
    # rlist = indices (in data/labels) of data points in a given subset of the data
    def _createTree(self, tree, pAttr, rlist):
        data = self._data
        labels = self._labels

        gains = [0 for i in range(len(pAttr))]

        for i in range(len(pAttr)):             # iterate over attribute array
            a = pAttr[i]                        # current attribute
            gains[i] = self._gain(a, rlist)

        print("\ngains = ")
        print(gains)
        maxGain = 0                             # index of max gain
        for i in range(len(gains)):
            if gains[i] > gains[maxGain]:
                maxGain = i

        tree.attr = pAttr[maxGain]
        del pAttr[maxGain]                      # remove attribute we're using from list

        tree.vals = list(self._counts[pAttr[maxGain]])
        tree.subTrees = [None for i in range(len(tree.vals))]
        tree.final_label = [None for i in range(len(tree.vals))]

        for i in range(len(tree.vals)):
            val = tree.vals[i]
            rlist2 = deepcopy(rlist)
            # create list of indices in data that are considered "remaining"

            tree.subTrees[i]
            tree.final_label[i]

            # check if all members of subset are in the same label, if so then stop
            # else recursively call for each possible value
            # remove data for each call that does not fit in that subtree



    # information gain for a specific attribute
    def _gain(self, a, rlist):
        print("\n...calculating gain for attribute " + str(a))
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
        data = self._data
        labels = self._labels
        total = 0.0

        # list of subsets split on each value of the attribute
        # a subset is represented as a list of relevant indices in data/labels
        vals = {}

        for i in rlist:
            # i is the relevant index of a data point
            p = data[i]                         # current data point (vector)
            val = p[a]
            if not val in vals:
                vals[val] = []
            vals[val].append(i)

        # iterate over each subset
        for val in vals:
            # subset of the (remaining) data such that every elemen has value val for attribute a
            sub = vals[val]
            s_v = len(sub)
            sub_entropy = self._entropy(sub)

            total += -1 * s_v / len(rlist) * sub_entropy

        print("expected entropy = " + str(total))
        return total


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


    # get proportion of a specific label value amongst all (remaining) data points
    def _getLabelProportion(self, lbl, label_count, numPoints):
        if not lbl in label_count:
            return 0.0
        return label_count[lbl] / numPoints;    # ratio of (remaining) data points with this label


    # classify a vector (after training has been completed)
    def classify(self, x):
        pass
