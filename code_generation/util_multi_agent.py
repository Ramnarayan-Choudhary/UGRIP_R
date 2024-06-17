# Utility functions for multi-agent conversation
# Teacher and student clients

import os
from openai import AzureOpenAI
import datetime
import json
import subprocess
import re

def load_model(model_name):
    print(f"Loading {model_name}...")
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key="037155e1b16a432fa836637370eca0e3",
        api_version="2024-02-15-preview"
    )
    print("SUCCESS: model loaded.")
    return client


class Conversation:
    def __init__(self, client, model_name, role):
        self.role = role
        self.client = client
        self.model_name = model_name
        self.resp_dict = {}
        self.msg_text = []
        self.prev_resp = ""
        self.idx = 0

    def process(self, prompt, max_tokens=300):
        self.msg_text.append({"role": "system", "content": self.prev_resp})
        self.msg_text.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.msg_text,
            temperature=0,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        resp_content = completion.to_dict()['choices'][0]['message']['content']
        self.resp_dict[f'Prompt {self.idx + 1}'] = resp_content
        self.prev_resp = resp_content
        self.idx += 1
         
        return resp_content
        # print(f"SUCCESS: prompt {self.idx} is processed.")

    def __str__(self):
        return f"{self.role} Answer {self.idx}: {self.prev_resp}"


class ScriptHelper:
    def __init__(self):
        pass

    def save_to_file(self, script_string, file_name):
         # Use regex to find the content between '''python ... ''' or ```python ... ```
        pattern = re.compile(r"```python\s*(.*?)```", re.DOTALL | re.MULTILINE)
        match = pattern.search(script_string)
        
        if match:
            clean_script = match.group(1).strip()
        else:
            # If no match is found, assume the script_string is already clean
            clean_script = script_string.strip()
        
        # Save the cleaned script to a file
        with open(file_name, 'w') as file:
            file.write(clean_script)

    def run_script(self, file_name):
        # Run the script using subprocess and collect the output
        result = subprocess.run(['python', file_name], capture_output=True, text=True)
        return result.stdout, result.stderr


def create_template_code_string(file_path):
    # Read the content of the Python file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    print(content)

    replacement01 = '''def encrypt_sentence(sentence):

    # TODO: Construct the "new_sentence" that can encrypt each sentence from "examples".
    
    return new_sentence
'''

    replacement02 = '''with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)
'''

    # Match and replace
    pattern01 = re.compile(r'def encrypt_sentence\(sentence\).*?return new_sentence\n', re.DOTALL)
    new_content = re.sub(pattern01, replacement01, content)

    pattern02 = re.compile(r'with open\("teacher_examples\.json", "w", encoding=\'utf-8\'\) as json_file:.*?print\("SUCCESS: teacher json files created."\)', re.DOTALL)
    new_content = re.sub(pattern02, replacement02, new_content)

    return new_content
