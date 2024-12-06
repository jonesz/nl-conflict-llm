#!/usr/bin/python
import argparse
import json

def fetch_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser

if __name__ == "__main__":
    args = fetch_parser().parse_args()
    with open(args.filename, 'r') as f:
        report = json.load(f)

        for elem in report:
            print(elem['prompt'])
            print(f"expecting: {elem['result']}")

            for response in elem['responses']:
                x = input()
                print(response['response'])
