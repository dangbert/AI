class Cluster:
    def __init__(self):
        self.center = []
        self.members = []                       # indicies of the data points in this cluster
        self._oldMembers = []                  # indicies of the data points in this cluster


    # add a data member index
    def add (self, index):
        self.members.append(index)


    def reset(self):
        self._oldMembers = self.members
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


    # recalculate the center
    def recalculate(self, data):
        # TODO: handle when the cluster is empty (no members)
        print("\nrecalculating")
        print(self.members)
        size = len(data[self.members[0]])
        mean = [0] * size
        for val in self.members:
            point = data[val]
            for i in range(size):
                mean[i] += point[i]

        # convert totals to means
        for val in mean:
            val = val / len(self.members)
        print("old center: " + str(self.center))
        self.center = mean
        print("       new: " + str(self.center))
