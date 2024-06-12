# UGRIP IOL Problem
# Experiment: Translate to various "global soucre" languages and compare
# Apply distance metrics

# Updated 06/12/2024
# Sample language: Madak

import json
import os
from util_prompt_cration import *


def read_json_file_as_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data

def extract_json_content(json_data):
    source_lang = json_data.get("source_language", "")
    target_lang = json_data.get("target_language", "")
    
    train_content = '{"train": ' + json.dumps(json_data.get("train", []), indent=2) + '}'
    test_content = '{"test": ' + json.dumps(json_data.get("test", []), indent=2) + '}'
    
    return source_lang, target_lang, train_content, test_content

# file_path = os.path.join("input_problem_set", "7961_madak_test.json")
# file_path = os.path.join("input_problem_set", "b188_chickasaw.json")
file_path = os.path.join("input_problem_set", "3ffc_norwegian.json")

# Example usage:  # Replace with the path to your JSON file
json_data = read_json_file_as_string(file_path)

source_lang, target_lang, train_content, test_content = extract_json_content(json_data)

prompt = create_puzzling_prompt(train_content, test_content)
formatted_prompt = create_chatbot_prompt(prompt, test_content)

input_prompt_dir = os.path.join('input_prompts', 'joy_prompt.txt')
with open(input_prompt_dir, 'w', encoding='utf-8') as file:
    file.write(formatted_prompt)

print(f"\nSUCCESS: Prompt saved at {input_prompt_dir}\n")