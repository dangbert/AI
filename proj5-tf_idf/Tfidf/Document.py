
# TODO: note that string.punctuation exists: https://www.geeksforgeeks.org/string-punctuation-in-python/
SYMBOLS = [
    '~',
    '`',
    '!',
    '@',
    '#',
    '$',
    '%',
    '^',
    '&',
    '*',
    '(',
    ')',
    '-',
    '_',
    '+',
    '=',
    '{',
    '}',
    '[',
    ']',
    '|',
    '\\',
    ':',
    ';',
    '\'',
    '"',
    ',',
    '.',
    '<',
    '>',
    '?',
    '/',
    '€',
]
SYMBOLS_STR = ''.join(SYMBOLS)

class Document:
    """Tracks a list of words (and their distributions) within a single file."""

    def load(self, input_file, ignoreCase=True, stripSymbols=True):
        """read input_file and store stats."""
        self._name = input_file
        self._dist = {}                         # word distribution
        self._numWords = 0

        f = open(input_file, "r")               # open file for reading
        for line in f:
            # split each line (by space character) into an array
            words = list(line.split())

            self._numWords = len(words)
            for word in words:
                if ignoreCase:
                    word = word.lower()
                # strip symbols:
                if stripSymbols:
                    word = ''.join(c for c in word if c not in SYMBOLS_STR)
                word = word.strip()
                if word not in self._dist:
                    self._dist[word] = 0
                self._dist[word] += 1
        f.close()

    def contains(self, word):
        """return True if this Document contains the given word."""
        return word in self._dist

    def getTf(self, word):
        """return the term frequency (float in range [0,1]) of a given word in this Document."""
        if word not in self._dist or self._numWords == 0:
            return 0
        return self._dist[word] / self._numWords
