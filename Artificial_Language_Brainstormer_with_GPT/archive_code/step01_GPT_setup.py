import json
import os
import pickle
import datetime
from openai import AzureOpenAI

gpt_models = ["gpt35turbo", "gpt4"]

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

# Run the respective models
outputs = []
client = load_model()
prompts = ['Hi! What is your name?',
           'Can you create a language with me?',
           'Lets start with an alphabet. What is your favorite alphabet?']

response_dict = {}
for prompt in prompts:
    message_text = [{"role": "system", "content": ""}, {"role": "user", "content": prompt}]
    print(f"Sending prompt: {prompt}")
    completion = client.chat.completions.create(
        model='gpt35turbo',  # model = "deployment_name"
        messages=message_text,
        temperature=0.8,
        max_tokens=1024,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    response_content = completion.to_dict()['choices'][0]['message']['content']
    outputs.append(response_content)
    response_dict[prompt] = response_content
    print(f"Received response: {response_content}")

# Save to JSON file
timestamp = datetime.datetime.now().strftime("%H_%M_%S")
json_filename = f"output/GPT_response_{timestamp}.json"
os.makedirs("output", exist_ok=True)
with open(json_filename, 'w') as json_file:
    json.dump(response_dict, json_file, indent=4)
    print(f"Responses saved to {json_filename}")


print("All tasks completed successfully.")
