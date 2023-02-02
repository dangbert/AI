#!/usr/bin/python3

import argparse
import os
import glob
from typing import List
from collections import defaultdict
import re
import csv

DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = argparse.ArgumentParser(description="simply returns most common tokens found within a directory (or single file).")
    parser.add_argument('input_dir', type=str, help='path to directory to read files from (or just a single file)')
    parser.add_argument('-e', '--extensions', type=str, help='comma separted list of (case insensitive) file extensions e.g. "md,txt" (the default)', default="md,txt")
    parser.add_argument('-n', type=int, help='max num of keywords to extract from each file (default 10)', default=10)
    parser.add_argument('-v', '--verbose', action="store_true", help='print extra info while running (for debugging)', default=False)
    parser.add_argument('-o', '--output-csv', type=str, help='path to csv to store results')
    args = parser.parse_args()

    extensions = args.extensions.split(',')
    files: List[str] = []
    if os.path.isfile(args.input_dir):
        files = [args.input_dir]
    else:
        pattern = os.path.join(args.input_dir, '**/*')
        for fname in list(glob.glob(pattern, recursive=True)):
            if args.verbose:
                print(f"considering: '{fname}'")
            if not os.path.isfile(fname):
                continue
            baseName, ext = os.path.splitext(fname)
            ext = ext[1:] if len(ext) > 0 and ext[0] == '.' else ext
            if ext not in extensions:
                continue
            files.append(fname)


    print(f"searching {len(files)} files...")
    if args.verbose:
        #print(f"\t{files}")
        print(f"extensions = {extensions}")
    print('')

    data = defaultdict(int)
    for fname in files:
        with open(fname, 'r') as f:
            contents = str(f.readlines())
            splitIntoWords(contents, data)

    topWords = sorted(data.keys(), key=lambda x: data[x], reverse=True)
    total = sum(data.values()) # total number of non-unique words
    print(f"outputting top {args.n} tokens")
    for i in range(args.n):
        word = topWords[i]
        print(f"{str(i+1).zfill(3)}: {(data[word] / total * 100):.2f}%, '{word}'")

    if args.output_csv:
        with open(args.output_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['token', 'ratio'])

            for i in range(args.n):
                word = topWords[i]
                ratio = (data[word]) / total
                writer.writerow([word, f"{ratio:.4f}"])
        print(f"wrote {args.n} top tokens of ({len(data.keys())} total) to {args.output_csv}")




def splitIntoWords(contents: str, data: defaultdict):
    """
    Splits contents of a string into words, and updates their counts in data.
    This is an alternative to using my Document class (I'm not sure which approach is better).
    https://stackoverflow.com/a/65917726
    """
    word_regex_improved = r"(\w[\w']*\w|\w)"
    word_matcher = re.compile(word_regex_improved)
    for word in word_matcher.findall(contents):
        data[word.lower()] += 1

if __name__ == "__main__":
    main()
