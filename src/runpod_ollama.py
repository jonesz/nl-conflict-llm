#!/usr/bin/python
from ollama import Client
import ollama
import os
import json
import argparse
from datetime import datetime

# The number of times to fire each prompt (think temperature) for each component. 
COMPONENT_TEST_NO = 50

PROMPT_ZERO_SHOT_REALIZABLE_Y_N =  \
"""From this set of engineering requirements, I want you to assess whether there is requirement conflict (and thus, the system can't be built).
What follows is the set of requirements:

{}

Please answer with "conflict" if there is a conflict, and "no conflict" otherwise.
"""
    
# results = []
# times = []
# for (i, elem) in enumerate(ds[:25]):
#     print(i)
#     reqs = []
#     for e in elem["comb"]:
#         reqs.append(": ".join(e))
#     content = PROMPT_ZERO_SHOT_REALIZABLE_PICK.format("\n".join(reqs))
#        
#     # TODO: Temperature.
#     print(content)
#     try:
#         start = time.time()
#         response = client.generate(model="llama3.1:8b", prompt=content, stream=False)
#         print(response)
#         end = time.time()
#         times.append(end - start)
#     except ollama.ResponseError as e:
#         print(e)

def fetch_all_req_and_rationale(r_in):
    """Parse a realizability report and return the requirement/rationale as a key/value structure."""
    output_req = {}
    for req in r_in['systemComponents'][0]['requirements']:
        name = req['reqid']
        rationale = req['rationale']
        output_req[name] = rationale
    return output_req
    
def component_test(realizability_fname, model, client):
    """ Given some file, compute tests on the "monolithic component"; that is if there are
    7 requirements, all 7 requirements are included within the prompt. """

    test_results = []

    r_json = json.load(open(realizability_fname, 'r'))
    requirements = fetch_all_req_and_rationale(r_json)

    for component in r_json['systemComponents'][0]['compositional']['connectedComponents']:
        test_case = {}
        test_case["ccName"] = component["ccName"]
        test_case["result"] = component["result"]
        test_case["requirements"] = component['requirements']
        test_case["prompt"] = PROMPT_ZERO_SHOT_REALIZABLE_Y_N.format("\n".join(["{}: {}".format(req_id, requirements[req_id]) for req_id in component["requirements"]]))
        test_case["responses"] = []

        for i in range(0, COMPONENT_TEST_NO):
            response = "Error on iteration {}.".format(i)
            try:
                response = client.generate(model=model, prompt=test_case["prompt"], stream=False)
                print(response['response'])
            except ollama.ResponseError as e:
                print(e)

            test_case["responses"].append(response)
        test_results.append(test_case)
    return test_results

def combination_test(raw_realizability_file):
    """ Given some file, compute tests on the "combinations"; that is if there are 7 requirements,
    produce tests that are 7c2 or something. """
    pass

def ollama_client(runpod_id):
    """ Return an ollama client. """
    client = Client(host="https://{}-11434.proxy.runpod.net".format(runpod_id), timeout=100)
    return client

def fetch_parser():
    parser = argparse.ArgumentParser(
        prog="runpod_ollama",
        description="Run some test to an ollama endpoint on Runpod."
    )

    parser.add_argument('runpod_id')
    parser.add_argument('filename_in')
    parser.add_argument('model')
    return parser

if __name__ == "__main__":
    args = fetch_parser().parse_args()
    out_fname = "component_result_{}_{}_{}".format(args.filename_in, args.model, datetime.now()).replace("/", "_").replace(" ", "_")
    with open("component_reports/" + out_fname, 'w') as f:
        component_test_results = component_test(args.filename_in, args.model, ollama_client(args.runpod_id))
        json.dump(component_test_results, f)
