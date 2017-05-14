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
    # TODO: just set self._label when recalculate is called()
    def getLabel(self):
        #print("members: " + str(self.members))

        dist = {}                               # lable distribution
        for index in self.members:
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

        return best


    # TODO: consider merging with recalculate!
    def reset(self):
        self._oldMembers = deepcopy(self.members)
        self.members = []


    # returns true if members is different from oldMembers
    def isChanged(self):
        if len(self.members) != len(self._oldMembers):
            return True

        self.members.sort()
        self._oldMembers.sort()
        for i in range(len(self.members)):
            if self.members[i] != self._oldMembers[i]:
                return True
        return False


    # recalculate cluster center
    def recalculate(self):
        # handle when the cluster is empty (no members)
        if len(self.members) == 0:
            return

        #print("\nrecalculating")
        #print(self.members)
        size = len(self._data[self.members[0]])
        mean = [0] * size

        for val in self.members:
            x = self._data[val]
            for i in range(size):
                mean[i] += x[i]

        # convert totals to means
        #print("total: " + str(mean))
        #print("num members: " + str(len(self.members)))
        for i in range(len(mean)):
            mean[i] = mean[i] / len(self.members)
        #print("old center: " + str(self.center))
        self.center = mean
        #print("       new: " + str(self.center) + "\n")
