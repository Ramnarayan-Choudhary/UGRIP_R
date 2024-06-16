# Teacher and Student Interactions Util code and workflow
# Write this myself


# Required Helper Functions:
# 1. cient = load_model(model_name) -> sets up one single client
# 2. questions, answers = teacher_generate_lecture_materials(lang_rules) -> generates questions and answers

import os
from openai import AzureOpenAI
import datetime
import json

def main():
    model_name = 'gpt4'

    client01 = load_model(model_name)
    client02 = load_model(model_name)

    resp_dict01= {}
    msg_text01 = []
    prev_resp01 = ""
    i = 0

    resp_dict02= {}
    msg_text02 = []
    prev_resp02 = ""
    j = 0

    prompt = 'hello there, can you ask one funny question as a joke? Only state one question itself, nothing else.'

    # Ask question 1 to client 1
    resp_dict01, msg_text01, i, prev_resp01 = process_prompt(client01, model_name, 100, resp_dict01, 
                   msg_text01, prev_resp01, i, prompt)
    
    
    print(resp_dict01)
    print(msg_text01)
    print(prev_resp01)

    print('CLIENT 1 DONE WITH ITERATION {}\n'.format(i)) # i = 1

    # # Pass along client 1's answer to client 2
    ans_prompt01 = 'Hi, can you answer this question: ' + resp_dict01[f'Prompt {i}'] + 'Only list the answer in one sentence. No explanations needed.'
    
    print(ans_prompt01)
    resp_dict02, msg_text02, j, prev_resp02 = process_prompt(client02, model_name, 200, resp_dict02, 
                   msg_text02, prev_resp02, j, ans_prompt01)
    
    print(resp_dict02)
    print('CLIENT 2 DONE WITH ITERATION {}\n'.format(j)) # j = 1

    # Ask question 2 to client 1
    ans_prompt02 = "Did I answer this correctly?" + resp_dict02[f'Prompt {j}'] + 'Just say "yes" or "no".'
    resp_dict01, msg_text01, i, prev_resp01 = process_prompt(client01, model_name, 300, resp_dict01, 
                   msg_text01, prev_resp01, i, ans_prompt02)
    
    print(resp_dict01)
    print(msg_text01)
    print(prev_resp01) # YES

    # Ask client 2 to modify the question, then send to client 1
    ans_prompt03 = "Can you come up with another question about camels? Just ask the question in one sentence, nothing else."
    resp_dict02, msg_text02, j, prev_resp02 = process_prompt(client02, model_name, 300, resp_dict02, 
                   msg_text02, prev_resp02, j, ans_prompt03)
    
    print(resp_dict02)
    print(msg_text02)
    print(prev_resp02) # YES

    print('CLIENT 2 DONE WITH ITERATION {}\n'.format(i)) # j = 1

    # Ask question 2 to client 1
    ans_prompt04 = "Can you answer this quesion in one sentence?" + resp_dict02[f'Prompt {j}']
    resp_dict01, msg_text01, i, prev_resp01 = process_prompt(client01, model_name, 300, resp_dict01, 
                   msg_text01, prev_resp01, i, ans_prompt04)
    
    print(resp_dict01)
    print(msg_text01)
    print(prev_resp01) # YES
    print('CLIENT 1 DONE WITH ITERATION {}\n'.format(i)) # j = 1


    

    


# Load the specified LLM model
def load_model(model_name):
    print(f"Loading {model_name}...")
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key="037155e1b16a432fa836637370eca0e3",
        api_version="2024-02-15-preview"
    )
    print("SUCCESS: model loaded.")
    return client


# Function to process conversation and get resps
def process_prompt(client, model_name, max_tokens, resp_dict, msg_text, prev_resp, i, prompt):
    # resp_list = []
    # resp_dict = {}

    # prev_resp = "" 
    # msg_text = []  

    msg_text.append({"role": "system", "content": prev_resp})  
    msg_text.append({"role": "user", "content": prompt})  

    # print(f"Sending prompt: {prompt}")
    completion = client.chat.completions.create(
        model=model_name,  
        messages=msg_text,  
        temperature=0, # this could be 0 (reproduceable)
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    resp_content = completion.to_dict()['choices'][0]['message']['content']
    resp_dict[f'Prompt {i + 1}'] = resp_content
    prev_resp = resp_content
    i += 1

    print(f"SUCCESS: prompt {i + 1} is processed.")
    return resp_dict, msg_text, i, prev_resp




if __name__ == "__main__":
    main()


