class Tfidf:

    # constructor
    def __init__(self, fnames):
        self._data = []
        for name in fnames:
            self._readFile(name)
        print(self._data)


    # read data from the input file
    def _readFile(self, input_file):
        dist = {}                               # word distribution
        f = open(input_file, "r")               # open file for reading

        for line in f:
            # split each line (by space character) into array
            vals = list(line.split())

            for word in vals:
                if word not in dist:
                    dist[word] = 0
                dist[word] += 1

        f.close()
        self._data.append(dist)
