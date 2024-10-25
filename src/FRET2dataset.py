#!/usr/bin/python
import json
import argparse
import itertools

def parse_report(r):
    ## Generate pairs of REQ_ID, RATIONALE.
    req_list = []
    for elem in r['systemComponents'][0]['requirements']:
        name = elem["reqid"]
        rationale = elem["rationale"]

        # If there's no rationale, utilize the FRETish.
        if rationale.strip() == "": 
            rationale = elem["fulltext"]
        req_list.append((name, rationale))

    conflicts = []

    # FETCH ALL COMPONENT WISE CONFLICTS
    for component in r['systemComponents'][0]['compositional']['connectedComponents']:
        if "Conflicts" in component['diagnosisReport']:
            for conflict in component['diagnosisReport']['Conflicts']:
                conflicts.append(conflict['Conflict'])

    out = {"req_list": req_list, "conflicts": conflicts }
    return out

def produce_combinations(components, r):
    out = []
    for elem in itertools.combinations(components["req_list"], r):
        realizability = True
        r_ids = [] # Capture all the IDs used in this combination.
        for req in elem:
            r_ids.append(req[0][:3] + req[0][4:])
        conflicts = []
        for conflict in components["conflicts"]:
            tot = 0
            for conflict_req in conflict:
                if conflict_req in r_ids:
                    tot += 1
            if tot > 1:
                realizability = False
                conflicts.append(conflict)
        out.append({"comb": elem, "conflicts": conflicts, "realizability": realizability})
    return out

def fetch_parser():
    """ Build and return an argument parser for the program. """

    parser = argparse.ArgumentParser(
        prog="FRET2dataset",
        description="Convert a FRET realizability report to a dataset.",
    )

    parser.add_argument('filename')
    return parser


if __name__ == "__main__":
    parser = fetch_parser()
    args = parser.parse_args()

    realizability = parse_report(json.load(open(args.filename, "r")))
    r = 3
    with open(f"combinations_{r}.json", "w") as f:
        json.dump(produce_combinations(realizability, r), f)
