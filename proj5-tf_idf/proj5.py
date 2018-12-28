#!/usr/bin/python3
from Tfidf import Tfidf

files = ["apple.txt", "facebook.txt", "google.txt", "microsoft.txt", "tesla.txt"]

model = Tfidf(files)

for name in files:
    model.getTop(5, name, True)
    print()
