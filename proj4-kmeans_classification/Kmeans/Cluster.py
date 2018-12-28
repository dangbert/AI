from copy import deepcopy

class Cluster:
    # note this does a shallow copy of data and labels
    def __init__(self, data, labels):
        self._data = data
        self._labels = labels
        self.center = []
        self._members = []                      # indicies of the data points in this cluster
        self._oldMembers = []                   # indicies of the data points in this cluster
        self._label = None                      # label assigned to this cluster


    # add a data member to this cluster
    # index should be the index of the data member in self._data
    def add(self, index):
        self._members.append(index)


    # returns true if _members is different from oldMembers
    def isChanged(self):
        if len(self._members) != len(self._oldMembers):
            return True

        self._members.sort()
        self._oldMembers.sort()
        for i in range(len(self._members)):
            if self._members[i] != self._oldMembers[i]:
                return True
        return False


    # recalculate cluster center and overall label
    # also clear self._members in preparation for the next cycle
    def recalculate(self):
        self._setLabel()
        if len(self._members) == 0:             # handle when the cluster is empty (no members)
            self._resetPoints()
            return

        size = len(self._data[self._members[0]])
        mean = [0] * size

        for val in self._members:
            x = self._data[val]
            for i in range(size):
                mean[i] += x[i]

        # convert totals to means
        for i in range(len(mean)):
            mean[i] = mean[i] / len(self._members)
        self.center = mean

        self._resetPoints()


    # reset the cluster by "removing" it's data points
    # keep the old ones in _oldMembers so we can tell if the cluster actually changes later
    def _resetPoints(self):
        self._oldMembers = deepcopy(self._members)
        self._members = []


    # assign this cluster the most popular label among its data points
    def _setLabel(self):
        dist = {}                               # lable distribution
        for index in self._members:
            l = self._labels[index]
            if l not in dist:
                dist[l] = 0
            dist[l] += 1

        first = 1
        if len(dist) == 0:
            print("length 0")

        best = -1
        for key in dist:
            if first:
                first = 0
                best = key
            if dist[key] > dist[best]:
                best = key
        self.label = best
