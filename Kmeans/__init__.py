import math
from copy import deepcopy
from random import randint
from Kmeans import Cluster


# creates a decision tree based on training data
# uses the ID3 algorithm with maximum gain
class Kmeans:

    def train(self, data, labels, k):
        self._data = data
        self._labels = labels
        self._k = k

        # TODO: remove functions' (clusters) parameter later where possible

        remaining = deepcopy(self._data)
        self._clusters = self._generateInitial()

        changed = True
        # continue until the clusters stop changing
        while changed:
            #self._printClusters()
            #print("\n\n--- at top ---")

            # reset the clusters (remove their data points)
            self._resetClusters()

            # iterate over each data point
            # and add it to the nearest cluster
            for i in range(len(self._data)):
                x = self._data[i]
                clust = self._findClosest(x)
                clust.add(i)

            changed = self._wasChanged()
            if changed:
                #print("recalculating centers")
                self._calculateCenters()

        print("----training complete----\n\n\n")


    def _printClusters(self):
        print("\nCLUSTERS:")
        for i in range(self._k):
            print(self._clusters[i].center)
            print("points = " + str(len(self._clusters[i].members)))
            #print(self._clusters[i].getLabel())
            print("")


    # create k random clusters
    def _generateInitial(self):
        index = []
        initial = []

        # assumes k <= len(self._data)
        for i in range(self._k):
            r = randint(0, len(self._data))
            while r in index:
                r = randint(0, len(self._data))
            index.append(r)

        for i in range(len(index)):
            c = Cluster.Cluster(self._data, self._labels)
            c.center = self._data[index[i]]
            initial.append(c)

        return initial


    # remove all data points from the clusters in preperation for next cycle
    def _resetClusters(self):
        for c in self._clusters:
            c.reset()


    # remove all data points from the clusters
    def _calculateCenters(self):
        for c in self._clusters:
            c.recalculate()


    # returns the distance squared between two vectors
    # (no point in taking the square root)
    def _distance(self, x, center):
        #print("\n\tcalculating distance between ")
        #print("\t\t" + str(x))
        #print("\t\t" + str(center))
        total = 0
        for i in range(len(x)):
            total += math.pow(center[i] - x[i], 2)
        #print("\t\tdistance = " + str(total))
        return total


    # return True if one of the clusters was changed since the last cycle
    def _wasChanged(self):
        for c in self._clusters:
            if c.isChanged():
                return True
        return False


    # return the cluster closest to vector x
    def _findClosest(self, x, debug=0):
        # find the closest cluster
        closest = 0                             # index of closest cluster
        min = self._distance(x, self._clusters[0].center)
        if debug:
            print("\t" + str(min))

        for n in range(1, self._k):
            dist = self._distance(x, self._clusters[n].center)
            if debug:
                print("\t" + str(dist))
            if dist < min:
                min = dist
                closest = n

        if debug:
            print("\tmin: " + str(min) + "\t-> cluster " + str(closest))
        return self._clusters[closest]


    # classify a vector (after training has been completed)
    def classify(self, x):
        clust = self._findClosest(x)
        lbl = clust.getLabel()
        return lbl
