#!/usr/bin/python3

import argparse
import os
import glob
from Tfidf import Tfidf
from typing import List

DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = argparse.ArgumentParser(description="run tf-idf algorithm on a set of files to identify keywords")
    parser.add_argument('input_dir', type=str, help='path to directory to read files from')
    parser.add_argument('-e', '--extensions', type=str, help='comma separted list of (case insensitive) file extensions e.g. "md,txt" (the default)', default="md,txt")
    parser.add_argument('-n', type=int, help='max num of keywords to extract from each file (default 10)', default=10)
    parser.add_argument('-v', '--verbose', action="store_true", help='print extra info while running (for debugging)', default=False)
    args = parser.parse_args()

    extensions = args.extensions.split(',')
    files: List[str] = []    
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

    #files = ["apple.txt", "facebook.txt", "google.txt", "microsoft.txt", "tesla.txt"]
    model = Tfidf(files)

    for name in files:
        res = model.getTop(args.n, name, print_results=True)
        print()

if __name__ == "__main__":
    main()
