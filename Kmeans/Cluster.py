from copy import deepcopy

class Cluster:
    # note this does a shallow copy of data and labels
    def __init__(self, data, labels):
        self._data = data
        self._labels = labels
        self.center = []
        self.members = []                       # indicies of the data points in this cluster
        self._oldMembers = []                   # indicies of the data points in this cluster


    # add a data member index
    def add(self, index):
        self.members.append(index)


    # get most popular label of this cluster
    def getLabel(self):
        dist = {}                               # lable distribution
        for index in self.members:
            l = self._lables[index]
            if l not in dist:
                dist[l] = 0
            dist[l] += 1

        best = dist.keys()[0]
        for key in dist:
            if dist[key] > dist[best]:
                best = key

        return best


    # TODO: consider merging with recalculate!
    def reset(self):
        self._oldMembers = deepcopy(self.members)
        self.members = []


    def isChanged(self):
        if len(self.members) != len(self._oldMembers):
            return True

        self.members.sort()
        self._oldMembers.sort()
        for i in range(len(self.members)):
            if self.members[i] != self._oldMembers[i]:
                return True
        return False


    def recalculate(self):
        # handle when the cluster is empty (no members)
        if len(self.members) == 0:
            self.center = None
            return

        print("\nrecalculating")
        print(self.members)
        size = len(self._data[self.members[0]])
        mean = [0] * size
        for val in self.members:
            point = self._data[val]
            for i in range(size):
                mean[i] += point[i]

        # convert totals to means
        for val in mean:
            val = val / len(self.members)
        print("old center: " + str(self.center))
        self.center = mean
        print("       new: " + str(self.center))
