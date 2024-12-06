#!/usr/bin/python
import argparse
import json
import re

# https://en.wikipedia.org/wiki/F-score
def f1(tp, fp, fn):
    return (2 * tp) / ((2 * tp) + fp + fn)

def is_realizable(line):
    conflict_pattern = r'\bconflict\b'
    no_conflict_pattern = r'\bno conflict\b'

    # These will count with overlap.
    conflict_sz = len(re.findall(conflict_pattern, line, re.IGNORECASE))
    no_conflict_sz = len(re.findall(no_conflict_pattern, line, re.IGNORECASE))

    # Figure this one out.
    # assert((conflict_sz > 0) or (no_conflict_sz > 0))

    # Remove the no conflict occurence from conflict; if there are more no conflicts.
    return no_conflict_sz > (conflict_sz - no_conflict_sz)

def fetch_parser():
    """ Build and return an argument parser for the program."""

    parser = argparse.ArgumentParser(
        prog="component_to_f1"
    )

    parser.add_argument('filename')
    return parser

if __name__ == "__main__":
    parser = fetch_parser()
    args = parser.parse_args()

    report = json.load(open(args.filename, "r"))

    tp = 0
    fp = 0
    fn = 0

    for elem in report:
        expected_result = (elem['result'] == "REALIZABLE")
        for response in elem['responses']:
            llm_result = is_realizable(response['response'])

            if expected_result == True and llm_result == True:
                tp += 1
            if expected_result == False and llm_result == True:
                fp += 1
            if expected_result == True and llm_result == False:
                fn += 1

    print(f"F1 for {args.filename}: {f1(tp, fp, fn)}")
