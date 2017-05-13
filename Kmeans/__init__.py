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

        remaining = deepcopy(self._data)
        clusters = self._generateInitial()

        changed = True
        while changed:
            print("\n\n--- at top ---")
            # reset the clusters (delete their data points)
            self._resetClusters(clusters)

            for i in range(len(self._data)):
                x = self._data[i]
                # find the closest cluster
                closest = 0                     # index of closest cluster
                min = self._distance(x, clusters[0].center)

                for n in range(1, self._k):
                    dist = self._distance(x, clusters[n].center)
                    if dist < min:
                        dist = min
                        closest = n

                clusters[closest].add(i)
            changed = self._wasChanged(clusters)
            if changed:
                print("recalculating centers")
                self._calculateCenters(clusters)


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
    def _resetClusters(self, clusters):
        for c in clusters:
            c.reset()


    # remove all data points from the clusters
    def _calculateCenters(self, clusters):
        for c in clusters:
            c.recalculate()


    # returns the distance squared between two vectors
    def _distance(self, x, center):
        total = 0
        for i in range(len(x)):
            total += math.pow(center[i] - x[i], 2)
        return total


    # return True if one of the clusters was changed since the last cycle
    def _wasChanged(self, clusters):
        for c in clusters:
            if c.isChanged():
                return True
        return False


    # classify a vector (after training has been completed)
    def classify(self, x):
        print("in classify")
