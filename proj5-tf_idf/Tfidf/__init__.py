# Dan Engbert
# CMSC 471 - Spring 2017

from Tfidf import Document
from math import log
from copy import deepcopy
import operator

class Tfidf:

    # constructor
    # fnames is an array of strings (file names)
    def __init__(self, fnames):
        self._docs = {}
        self._names = deepcopy(fnames)
        for name in fnames:
            doc = Document.Document()
            doc.load(name)
            self._docs[name] = doc


    # return an array of tuples of the top n words in a doc and their tfidf values
    def getTop(self, n, fname, print_results=False):
        doc = self._docs[fname]
        vals = {}                               # {word: tfidf_val, ...}

        for word in doc._dist:
            vals[word] = self._tfidf(word, doc)

        # create array of tuples
        arr = sorted(vals.items(), key=operator.itemgetter(1))
        arr.reverse()
        arr = arr[:n]                           # get the first n elements of the array

        if print_results:
            print(f"'{fname}' top {len(arr)} words:")
            for tup in arr:
                s = "{:.5f}".format(tup[1])
                print(f"'{tup[0]}'\t(TF_IDF: {s})")

        return arr


    # computes the tfidf of a given word within a document
    def _tfidf(self, word, doc):
        return doc.getTf(word) * self._idf(word)


    # get the inverse document frequency of a given word
    def _idf(self, word):
        num = 0                                 # number of documents containing the word
        for key in self._docs:
            doc = self._docs[key]
            if doc.contains(word):
                num += 1

        return log(len(self._names) / num)
