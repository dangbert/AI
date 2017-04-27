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

        # TODO: consider requiring the user to give the range of expected attribute values
        # e.g. a dict where each key is an attribute and it pairs with the highest value it can take on

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
        # check if all members of subset are in the same label
        first_label = self._labels[rlist[0]]
        for r in range(1, len(rlist)):
            i = rlist[r]
            # i is the relevant index of a data point
            lbl = self._labels[i]
            if lbl != first_label:
                break
            if r == (len(rlist) - 1):
                tree.final_label = first_label
                print("**** at a stopping point ***")
                return

        if len(pAttr) == 0:
            print("\nno attributes left!")
            tree.chooseBest(self._getLabelCount(rlist))
            return

        gains = [0 for i in range(len(pAttr))]

        for i in range(len(pAttr)):             # iterate over attribute array
            a = pAttr[i]                        # current attribute
            gains[i] = self._gain(a, rlist)

        print("\nrlist:")
        for i in rlist:
            print(str(i) + "-> " + str(self._labels[i]) + "\t" + str(self._data[i]))
        print("gains = ")
        print(gains)
        print("pAttr = ")
        print(pAttr)
        maxGain = 0                             # index of max gain
        for i in range(len(gains)):
            if gains[i] > gains[maxGain]:
                maxGain = i

        # if all gains are 0 stop branching and use the most popular label
        # (in some data sets there may be duplicate vectors with different classifications)
        if gains[maxGain] == 0:
            # set tree label to the most popular option amongst the remaining data points
            tree.chooseBest(self._getLabelCount(rlist))
            return

        # TODO: should this be pAttr[maxGain]? yes!!!
        tree.attr = pAttr[maxGain]              # attribute number to split on
        print("decided to split on attribute " + str(tree.attr))
        del pAttr[maxGain]                      # remove attribute we're using from list


        tree.subTrees = [None for i in range(len(tree.vals))]
        tree.final_label = [None for i in range(len(tree.vals))]

        # TODO: avoid having to call this function twice???
        vals_dist = self._valDistribution(tree.attr, rlist)
        if len(pAttr) < 5:
            print("vals_dist = ")
            print(vals_dist)

        # possible (remaining) vals for this attribute to take on
        tree.vals = list(vals_dist)

        #print(vals_dist)
        #print("tree.vals = ")
        #print(tree.vals)

        tree.subTrees = [Tree.Tree() for i in range(len(tree.vals))]
        # iterate over each value to branch off of
        # recursively create tree for each possible value taken on by the attribute
        for i in range(len(tree.vals)):
            self._createTree(tree.subTrees[i], pAttr, vals_dist[tree.vals[i]])


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
            # subset of the (remaining) data such that every elemen has value val for attribute a
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


    # get proportion of a specific label value amongst all (remaining) data points
    def _getLabelProportion(self, lbl, label_count, numPoints):
        if not lbl in label_count:
            return 0.0
        return label_count[lbl] / numPoints;    # ratio of (remaining) data points with this label


    # classify a vector (after training has been completed)
    def classify(self, x):
        pass
