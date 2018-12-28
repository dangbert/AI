class Document:

    # read data from the input file
    def load(self, input_file):
        self._name = input_file
        self._dist = {}                         # word distribution
        self._numWords = 0

        f = open(input_file, "r")               # open file for reading
        for line in f:
            # split each line (by space character) into an array
            words = list(line.split())

            self._numWords = len(words)
            for word in words:
                if word not in self._dist:
                    self._dist[word] = 0
                self._dist[word] += 1
        f.close()


    def contains(self, word):
        return word in self._dist


    # return the term frequency of a given word in this document
    def getTf(self, word):
        if word not in self._dist:
            return 0
        return self._dist[word] / self._numWords
