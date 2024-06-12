# Util functions for the GPT API Playgorund
# Parse well-formed prompts from a .txt file
# Process the prompts using Chat-GPT API

import os
from openai import AzureOpenAI
import datetime
import json
from openai import AzureOpenAI

# Load the specified LLM model
def load_model():
    print("Loading the model...")
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key="037155e1b16a432fa836637370eca0e3",
        api_version="2024-02-15-preview"
    )
    print("Model loaded successfully.")
    return client


# Function to read conversation data from a .txt file
def read_convo_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    prompts = []
    current_prompt = ""
    is_prompt = False

    for line in lines:
        if line.startswith(">>>> Prompt"):
            is_prompt = True
            if current_prompt:
                prompts.append(current_prompt.strip())
            current_prompt = ""  # Reset current_prompt without adding the ">>>> Prompt" line
        elif line.startswith(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"):
            is_prompt = False
            if current_prompt:
                prompts.append(current_prompt.strip())
            current_prompt = ""
        elif line.startswith("--------") or line.startswith(">>>>---------"):
            is_prompt = False
            current_prompt = ""
        elif is_prompt:
            current_prompt += line

    if current_prompt:
        prompts.append(current_prompt.strip())
    
    return prompts


# Function to process conversation and get responses
def process_prompts(prompts, client, max_tokens=300):
    response_list = []
    response_dict = {}
    context = ""
    prev_response = ""

    message_text = []
    for i, prompt in enumerate(prompts):

        message_text.append({"role": "system", "content": prev_response})
        message_text.append({"role": "user", "content": prompt})

        # print(f"Sending prompt: {prompt}")
        completion = client.chat.completions.create(
            model='gpt35turbo',  # model = "deployment_name"
            messages=message_text,
            temperature=0.8, # this could be 0 (reproduceable)
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        response_content = completion.to_dict()['choices'][0]['message']['content']
        response_list.append(response_content)
        response_dict[f'Prompt {i+1}'] = response_content

        prev_response = response_content

        print(f"SUCCESS: prompt {i+1} is processed.")

    return response_dict, response_list


def load_file_as_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def fill_responses_in_text(text_content, responses):
    for i in range(len(responses)):
        placeholder = f'[insert respone {i+1}]'
        text_content = text_content.replace(placeholder, responses[i])
    return text_content


def save_convo_to_json(response_dict, input_prefix, timestamp):
    json_filename = f"output_json/{input_prefix}_GPT_convo.json"
    os.makedirs("output_json", exist_ok=True)
    try: 
        with open(json_filename, 'w') as json_file:
            json.dump(response_dict, json_file, indent=4)
            print(f"SUCCESS: Conversation JSON saved to {json_filename}")
    except FileNotFoundError:
        print(f"Error: File '{json_filename}' not found.")


def save_convo_to_txt(input_file, input_prefix, responses, timestamp):
    txt_content = load_file_as_string(input_file)
    output_text = fill_responses_in_text(txt_content, responses)
    output_report_filename = f'output_convos/{input_prefix}_GPT_convo.txt'
    os.makedirs("output_convos", exist_ok=True)
    try:
        with open(output_report_filename, 'w', encoding='utf-8') as file:
            file.write(output_text)
        print(f"SUCCESS: Conversation TXT saved to {output_report_filename}")
    except FileNotFoundError:
        print(f"Error: File '{output_report_filename}' not found.")

