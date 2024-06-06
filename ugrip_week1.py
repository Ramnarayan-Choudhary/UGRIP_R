# ugrip_week1.py
# Re-factored and updated 14:00 PM on 06/06/2024

from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from transformers import pipeline
import torch
import requests
import zipfile
import io
import os
import json
import datetime
from vllm import LLM, SamplingParams
from openai import OpenAI, AzureOpenAI
from huggingface_hub import login

# Config info 
gpt_models = ["gpt35turbo", "gpt4"]
open_source_models = ["meta-llama/Meta-Llama-3-70B-Instruct", "meta-llama/Meta-Llama-3-8B-Instruct",'TheBloke/Llama-2-7b-Chat-AWQ']
hf_token =  "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" 

''' Note: disabled time stamps for now '''
# timestamp = datetime.datetime.now().strftime("%H_%M_%S_%m_%d")
# path_out = f"outputs_{timestamp}"

path_out = f"outputs"
path_puzzling_data = "inputs_dataset"

# Create folder if it doesn't exist
def check_path(target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print(f"Created folder: {target_path}")

check_path(path_out)
check_path(path_puzzling_data)


def use_llm(json_tag, source_language, prompt_names, prompts, model_name, llm):
    '''
    This function uses the LLM model to generate translations/responses for the given prompts.
    
    Parameters:
    - json_tag: The 4-digit tag used for the output file name.
    - source_language: The source language for translation.
    - prompt_names: A list of prompt names.
    - prompts: A list of format strings of the populated templates.
    - model_name: The name of the model to be used.

    Returns:
    - None

    Mistral: mistralai/Mistral-7B-v0.1  [consider using more recent version of Mistral?]
    LLaMA: meta-llama/Meta-Llama-3-70B-Instruct [check if right ver?]                         
    list of supported LLMs: https://docs.vllm.ai/en/latest/models/supported_models.html#supported-models
    '''
    
    # Call LLMs or use dummy outputs
    model_type = '' # defualt directory prefix

    # Run the respective models
    if model_name in gpt_models:
        model_type = 'gpt'
        outputs = []
        client = load_model(model_name) # [?] Does this need to be called in a for loop?
        for prompt in prompts: 
            message_text = [{"role":"system","content":""}, {"role":"user", "content": prompt}]
            completion = client.chat.completions.create(
                model=model_name, # model = "deployment_name"
                messages = message_text,
                temperature=0.8, #TODO: change to 0.8 to be consistent? -a
                max_tokens=2048,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            outputs.append(completion.to_dict()['choices'][0]['message']['content'])

    elif model_name in open_source_models:
        model_type = 'open-source'
        sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=2048)
        outputs = llm.generate(prompts, sampling_params)

    else: # If we skip over llm, use dummy outputs
        model_type = 'dummy'
        outputs = ['output01', 'output02', 'output03']

    # Deal with each output, then create:
    # "outputs_[time_stamp]\[prompt_name]\[4-digit tag]_[target_language].txt"
    # Example: "outputs_19_22_37_06_05/base_prompt_puzzling/438d_turkish.txt"
    for idx, output in enumerate(outputs):
        prompt_name = prompt_names[idx]
        if model_name in gpt_models:
            generated_text = output
        elif model_name in open_source_models:
            prompt = output.prompt
            generated_text = output.outputs[0].text
        else: 
            prompt = "dummy_prompt_content"
            generated_text = f'dummy output: {output}'

        # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

        # prepare the new output path
        os.makedirs(os.path.join(path_out, model_type, prompt_name), exist_ok=True)
        source_lang_str = source_language.rstrip().replace(" ", "_")
        out_filename = os.path.join(path_out, model_type, prompt_name, f'{json_tag}_{source_lang_str}.txt')
        
        # TODO: fix this f.write() to alignw with the .json
        with open(out_filename, "a+") as f:
            f.write(generated_text + "\n")
            print(f"SUCCESS: {out_filename} is saved.")
    print('\n')

# Populate some prompt templates, then return
# - prompt_names: A list of prompt names (such as "base_prompt_puzzling", "longer_prompt_puzzling", etc.)
# - prompts: A list of format strings of the populated templates
def create_puzzling_prompt(language, data, eng_to_lang, lang_to_eng):

        #-----------------------------------
    # base_prompt_puzzling_old = f"""This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    # {data}

    # Given the above expressions, please translate the following statements:
    # a) from English into {language}
    # {eng_to_lang}

    # b) from {language} into English.
    # {lang_to_eng}""".format(language, data, eng_to_lang, lang_to_eng)

    #-----------------------------------

    base_prompt_puzzling = f"""This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    {data}

    Given the above expressions, please translate the following statements:
    a) from English into {language}
    {eng_to_lang}

    b) from {language} into English.




    {lang_to_eng}
  
    Please also provide your translation responses in the format of a JSON file. It should look like this: 

    "test": [
    [
    "translation sentence 1",
    "",
    "your response"
    ], 
    [
    "translation sentence 2",
    "",
    "your response"
    ], 
    ]

    where the translation sentences come from your tasks in part (a) and (b), and your translations for each of the sentences should be placed in the "your response" field. 

    """.format(language, data, eng_to_lang, lang_to_eng)


    
    #-----------------------------------
    # longer_prompt_puzzling_old = f"""This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    # Your task is to carefully analyze the expressions given, and use the information from them to translate some new statements. 
    # All of the information you need to do this task can be obtained from the given expressions. 





    # {data}

    # Given the above expressions, please translate the following statements:
    #  a) from English into {language}
    #  {eng_to_lang}

    #  b) from {language} into English.
    #  {lang_to_eng}""".format(language, data, eng_to_lang, lang_to_eng)
     
    # #-----------------------------------

    longer_prompt_puzzling = f"""This is a linguistics puzzle. Below are some expressions in the {language} language and their English translations. Your task is to carefully analyze the expressions given, and use the information from them to translate some new statements. This might involve logically reasoning about how words or parts of words are structured in {language}, what the word order could be, and how different grammatical phenomena could influence the expressions. 

    All of the information you need to do this task can be obtained from the given expressions. You do not need to use any external knowledge. 

    {data}

    Given the above expressions, please translate the following statements:
    a) from English into {language}
    {eng_to_lang}


    b) from {language} into English.
    {lang_to_eng}

    Please also provide your translation responses in the format of a JSON file. It should look like this: 

    "test": [
    [
    "translation sentence 1",
    "",
    "your response"
    ], 
    [
    "translation sentence 2",
    "",
    "your response"
    ], 
    ]

    where the translation sentences come from your tasks in part (a) and (b), and your translations for each of the sentences should be placed in the "your response" field. 

    """.format(language, data, eng_to_lang, lang_to_eng)


    #-----------------------------------
    
    cot_prompt_puzzling = f"""This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    Your task is to carefully analyze the expressions given, and use the information from them to translate some new statements. 
    All of the information you need to do this task can be obtained from the given expressions. 

    Let's think through this carefully step by step, using logical reasoning to infer the meanings of the words and get the correct answer. 

    {data}

    Given the above expressions, please translate the following statements:
     a) from English into {language}
     {eng_to_lang}

     b) from {language} into English.
     {lang_to_eng}

    Please also provide your translation responses in the format of a JSON file. It should look like this: 

    "test": [
    [
    "translation sentence 1",
    "",
    "your response"
    ], 
    [
    "translation sentence 2",
    "",
    "your response"
    ], 
    ]

    where the translation sentences come from your tasks in part (a) and (b), and your translations for each of the sentences should be placed in the "your response" field. 

    """.format(language, data, eng_to_lang, lang_to_eng)
    # [Manual Input]
    prompt_names = ['base_prompt_puzzling', 'longer_prompt_puzzling', 'cot_prompt_puzzling']
    prompts = [base_prompt_puzzling,
               longer_prompt_puzzling,
               cot_prompt_puzzling]
    
    return prompt_names, prompts

def create_puzzling_contamination_prompt(language, data, eng_to_lang, lang_to_eng):
    translate_without_context_prompt = f"""This is a linguistics puzzle. 

    Please translate the following statements to English:
    {lang_to_eng}
    """.format(language, data, eng_to_lang, lang_to_eng)

    ask_the_language_prompt = f"""This is a linguistics puzzle. 

    Please translate the following statements to English:

    Do you know what language this is? Please ONLY output the language without any additional explanation.
    {lang_to_eng}
    """.format(language, data, eng_to_lang, lang_to_eng)
    
    # [Manual Input]
    prompt_names = ['translate_without_context_prompt', 'longer_prompt_puzzling', 'cot_prompt_puzzling']
    prompts = [translate_without_context_prompt,
               ask_the_language_prompt]
    
    return prompt_names, prompts

# Populate the unique 4-digit tag for each problems, according to .json file names
def get_first_four_chars(filename):
    if '/' in filename:
        # Split by slash and get last element (filename)
        first_four_chars = filename.split("/")[-1][:4]
    else:
        # No slash, assume entire string is filename/extension
        first_four_chars = filename[:4]
    return first_four_chars


# Load data from the PuzzLing dataset .zip files
def init_puzzling_data():
    '''
    dataset format:
    a list of :
    'source_language'
    'target_language'
    'meta'
    'train' : a pair of source and target in a list
    'test' : a pair of source and target in a list (one is empty)
    '''

    # Path for the PuzzLing dataset to download
    url = 'https://ukplab.github.io/PuzzLing-Machines/data/public_data_dev.zip'
    directory = path_puzzling_data
    
    def download_and_extract_zip(url, directory):
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful

        # Create a ZipFile object from the response content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(directory)

    def read_puzzling_dataset(directory="None"):
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
        json_tags = []
        json_contents = []

        for file in json_files:
            file_path = os.path.join(directory, file)
            json_tag = get_first_four_chars(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_tags.append(json_tag)
                json_contents.append(data)

        return json_tags, json_contents

    # Download and extract the zip file
    download_and_extract_zip(url, path_puzzling_data)

    # this has all the problems
    puzzling_problem_tags, puzzling_problem_set = read_puzzling_dataset(directory)
    return puzzling_problem_tags, puzzling_problem_set

def init_puzzling_ground_truth():
    '''
    download answer from fround truth
    '''

    # Path for the PuzzLing dataset to download
    url = 'https://ukplab.github.io/PuzzLing-Machines/data/public_reference_data_dev.zip'
    directory = "puzzling_answer"
    
    def download_and_extract_zip(url, directory):
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful

        # Create a ZipFile object from the response content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(directory)
            
    download_and_extract_zip(url, directory)

    return ""

# Load a single JSON file and return the puzzling data
def init_puzzling_data_from_json(file_path):
    # for code dependency reasons, the outputs have to be a 1-element list
    json_tags = []
    json_contents = []
     
    json_tags.append(get_first_four_chars(file_path))
    with open(file_path, 'r') as f:
        json_contents.append(json.load(f))
    return json_tags, json_contents


# Load the speficied LLM model
def load_model(model_name):
    if model_name in gpt_models:
        client = AzureOpenAI(
            azure_endpoint = "https://cullmsouthindia.openai.azure.com/", 
            api_key="037155e1b16a432fa836637370eca0e3",  
            api_version="2024-02-15-preview"
        )
    elif model_name in open_source_models:
        login(token=hf_token)   
        client = LLM(model=model_name, quantization='AWQ')

    return client


# Prepare the prompts, then run the LLM model
def feed_problems_to_LLM(puzzling_problem_tags, puzzling_problem_set, model_name, is_contamination_check = False):
    llm = None
    if not model_name in gpt_models:
        llm = load_model(model_name)
    # pre-process and prompt preparation
    for idx, data in enumerate(puzzling_problem_set):
        source_language = data['source_language']
        # target_language = data['target_language'] # default in english
        # meta = data['meta'] # not really needed
        source = ""
        target = ""
        source_and_target = ""

        for item in data['train']:
            source += item[0] + "\n"
            target += item[1] + "\n"
            source_and_target += item[0] + "\t" + item[1] + "\n"
        
        eng_to_lang = ""
        lang_to_eng = ""
            
        for item in data['test']:
            if item[2] == "<":
                eng_to_lang += item[1] + "\n"
            else:
                lang_to_eng += item[0] + "\n"
                
        # prompts = create_puzzling_prompt(language=source_language, data=source_and_target, eng_to_lang=eng_to_lang, lang_to_eng=lang_to_eng)
        json_tag = puzzling_problem_tags[idx]
        if is_contamination_check:
            prompt_names, prompts = create_puzzling_contamination_prompt(language=source_language, data=source_and_target, eng_to_lang=eng_to_lang, lang_to_eng=lang_to_eng)
        else:
            prompt_names, prompts = create_puzzling_prompt(language=source_language, data=source_and_target, eng_to_lang=eng_to_lang, lang_to_eng=lang_to_eng)
        
        # Print human-readable prompts
        # print("-------------- PROMPT IS HERE ----------------")
        # for prompt in prompts:
        #     print('--------------- PROMPT LINE ---------------')
        #     print(prompt)
        #     print('--------------- DIV LINE')

        # Pass the prompts into llm
        use_llm(json_tag, source_language, prompt_names, prompts, model_name, llm)
    

# [TODO] [IN-PROGRESS] Load the phonological generalizations data
def init_phonological_generalizations_data(directory="None"):
    '''
    dataset format:
    a list of :
    'source_language'
    'target_language'
    'meta'
    'train' : a pair of source and target in a list
    'test' : a pair of source and target in a list (one is empty)
    '''
    url = 'https://github.com/saujasv/phonological-generalizations.git'
    json_dir = 'phonological-generalizations/data/problems'

    # Clone the repository if it does not exist
    if not os.path.exists(json_dir):
        os.system(f"git clone {url}")
    
    # Load all JSON files in the directory
    problems = []
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            with open(os.path.join(json_dir, filename), 'r') as file:
                problem_data = json.load(file)
                problems.append(problem_data)

    return problems


# [TODO] [IN-PROGRESS] ???
def transform_data(problems):
    transformed_data = []

    for problem_data in problems:
        source_language = problem_data.get('languages', [''])[0]  # Assuming the first language as source
        target_language = problem_data.get('languages', [''])[1] if len(problem_data.get('languages', [])) > 1 else ''  # Assuming the second language as target
        meta = {
            'families': problem_data.get('families', []),
            'type': problem_data.get('type', ''),
            'notes': problem_data.get('notes', '')
        }
        
        train_data = []
        test_data = []

        for row in problem_data.get('data', []):
            source = row[0] if len(row) > 0 else ''
            target = row[1] if len(row) > 1 else ''
            train_data.append([source, target])

        transformed_data.append({
            'source_language': source_language,
            'target_language': target_language,
            'meta': meta,
            'train': train_data,
            'test': test_data  
        })

    return transformed_data


# [TODO] [IN-PROGRESS] ???
def phonological_generalizations_data_loader(transformed_data):
    for data in transformed_data:
        source_language = data['source_language']
        target_language = data['target_language']
        meta = data['meta']

        source = ""
        target = ""
        source_and_target = ""

        for item in data['train']:
            source += item[0] + "\n"
            target += item[1] + "\n"
            source_and_target += item[0] + "\t" + item[1] + "\n"


def main():
    # [INPUT] This could be any of the GPTs or Llama models. Ex: 'gpt-35-turbo'
    # model_name = 'meta-llama/Meta-Llama-3-70B-Instruct' TheBloke/Llama-2-7b-Chat-AWQ
    # model_name = 'gpt-35-turbo'
    
    ''' If you don't want to use any model, use "dummy" as the model name.'''
    model_name = 'gpt35turbo' 
    model_name = 'meta-llama/Meta-Llama-3-8B-Instruct'

    # Toggle this for using .zip files or a single .json file
    bool_use_url_zip_files = True
    if bool_use_url_zip_files == True: # Loads all the PuzzLing dataset problems from the zip file 
        puzzling_data_tags, puzzling_problem_set = init_puzzling_data()
    else: # Use the local .json file [CAUTION] This only works on local machine rather than live code
        this_json_path = 'ed4b_tshluba_data.json'
        puzzling_data_tags, puzzling_problem_set = init_puzzling_data_from_json(this_json_path)
    
        # print(puzzling_data_tags)
        # print(puzzling_problem_set)
    feed_problems_to_LLM(puzzling_data_tags, puzzling_problem_set, model_name)


if __name__ == "__main__":
    main()
    
