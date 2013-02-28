#!/usr/bin/env python3

import os
import csv
import argparse
from collections import Counter

import ocreval.Dictionary as Dictionary
import ocreval.AccEval as AccEval

from pairtree import PairTreePathFinder 
from util import file_id_iter, require_py3


if __name__ == "__main__":

    require_py3()

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('COLLECTION',
                        help='Path to a HathiTrust collection.')
    parser.add_argument('OUTFILE', 
                        help='Desination file for CSV output.')
    parser.add_argument('IDFILE', 
                        nargs='?',
                        default=False,
                        help='Optional file of HathiTrust identifiers to evaluate. '
                        'Defaults to the entire collection.')

    args = parser.parse_args()

    collection = args.COLLECTION
    csvfile = args.OUTFILE
    idfile = args.IDFILE

    ptp = PairTreePathFinder(collection)
    lexicon = Dictionary.BuildLexicon()
   
    if not idfile:
        # default identifier in collection
        idfile = os.path.join(collection, 'id')

    scores = {}
    counter = Counter()
    with open(csvfile, 'w', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf)
        for i, htid in enumerate(file_id_iter(idfile, 'r')):
            try:
                path, post = ptp.get_path_to_htid(htid)
            except ValueError as ve:
                print(ve)
                continue
            path = os.path.join(path, post + ".txt")
            try:
                with open(path, encoding='utf-8') as f:
                    text = f.readlines()

                _,_,_,lowcount,lowmatch,_ = AccEval.GetScore(text, lexicon)
                pct = lowmatch / lowcount * 100
                pct = round(pct, 1)
                scores[htid] = pct
                counter[pct] += 1
                csvwriter.writerow([htid, pct])
                print(i, htid, pct)

            except IOError:
                pass

