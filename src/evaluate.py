from openai import OpenAI
import os
import json

PROMPT_ZERO_SHOT_REALIZABLE_Y_N =  \
"""I have a set of engineering requirements. I want you to determine if any of the requirements
conflict and thus make the project unrealizable. Please answer with "realizable" if the project
is realizable and no requirements conflict, or "unrealizable" if this isn't the case.

Here are the list of requirements. 

{}

Remember to answer with only "realizable" or "unrealizable".
"""

PROMPT_ZERO_SHOT_REALIZABLE_PICK = """
    I have a set of engineering requirements. I want you to determine if any of the requirements
    conflict and thus make the project unrealizable. Please answer with "realizable" if the project
    is realizable and no requirements conflict. If there are conflicts, please list the names of the
    requirements that conflict.

    Here are the list of requirements. 

    {}
    """

PROMPT_ZERO_SHOT_REALIZABLE_PICK_EXPLAIN = """
    I have a set of engineering requirements. I want you to determine if any of the requirements
    conflict and thus make the project unrealizable. Please answer with "realizable" if the project
    is realizable and no requirements conflict. If there are conflicts, please list the names of the
    requirements that conflict and give a short explanation of why they conflict, potentially with
    an example case that displays the conflict.

    Here are the list of requirements. 

    {}
    """

RUNPOD_API_KEY = "NULL"
RUNPOD_ENDPOINT_ID = "NULL"
    
client = OpenAI(
    api_key = RUNPOD_API_KEY,
    base_url=f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/openai/v1",
)

ds = json.load(open('combinations_3.json', 'r'))

results = []
for (i, elem) in enumerate(ds[:25]):
    print(i)
    reqs = []
    for e in elem["comb"]:
        reqs.append(": ".join(e))
    content = PROMPT_ZERO_SHOT_REALIZABLE_Y_N.format("\n".join(reqs))
       
    chat_completion = client.chat.completions.create(
        model="mistralai/Mistral-Small-Instruct-2409",
        messages=[{"role": "user", "content": content}])
    print(chat_completion)
    results.append((content, elem["realizability"], chat_completion.choices[0].message.content))

json.dump(results, open("results_llama-3.1-8b.json", "w"))
