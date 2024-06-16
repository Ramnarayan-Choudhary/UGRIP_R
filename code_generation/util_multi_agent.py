# Utility functions for multi-agent conversation
# Teacher and student clients

import os
from openai import AzureOpenAI
import datetime
import json
import util_python_formatter as pyform

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