class Tree:
    def __init__(self):
        self.attr = None                        # attribute index to use
        # the (child) branches

        # consider maybe making this a dict of val: <index of subtree>
        self.vals = []
        # TODO Initialize array to Nones?
        self.subTrees = []
        self.final_label = None


    def chooseBest(self, label_count):
        best = list(label_count)[0]
        for lbl in label_count:
            if label_count[lbl] > label_count[best]:
                best = lbl

        #print("label_count = " + str(label_count))
        #print("\nall gains are 0, using label " + str(best))
        self.final_label = best


    def getRelevantSubtree(self, val):
        for i in range(len(self.vals)):
            if val == self.vals[i]:
                return self.subTrees[i]
        #print("returning none")
        return None
