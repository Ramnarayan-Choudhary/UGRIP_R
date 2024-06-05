# ugrip_week1.py
# Updated 06.05.2024 @20:00

test 
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

# [INPUT] whether we're running LLM or skipping it (generating dummy outputs)
bool_use_LLM = False
if bool_use_LLM == True:
    login(token="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")

# [?] What is this?
m = "mistralai/Mistral-7B-v0.1"

# Config variables
timestamp = datetime.datetime.now().strftime("%H_%M_%S_%m_%d")
path_out = f"outputs_{timestamp}"
path_for_data = "inputs_dataset"

# Path for the PuzzLing dataset to download
url = 'https://ukplab.github.io/PuzzLing-Machines/data/public_data_test.zip'

# Create folder if it doesn't exist
def check_path(target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print(f"Created folder: {target_path}")

check_path(path_out)
check_path(path_for_data)


# setting up VLLM
# installed VLLM, OpenAI etc. packages on my conda UGRIP envt! 

def use_vllm(json_tag, source_language, prompt_names, prompts, model_name):
    '''
    this takes in a model and sets up VLLM to access it. 
    input string format: 

    Mistral: mistralai/Mistral-7B-v0.1  [consider using more recent version of Mistral?]
    LLaMA: meta-llama/Meta-Llama-3-70B-Instruct [check if right ver?] 
                                            
    For GPT models, need to query via OpenAI API.
    
    '''

    #antara prompting 

    #thought: different prompts for PuzzLing and Stress, because the problems are fundamentally kinda different
    
    '''
    PUZZLING


    Base prompt: 

    This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 

    {data}

    Given the above expressions, please translate the following statements:
     a) from English into {language}

     b) from {language} into English. 

    -----------

    More explanatory version: 

    This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    Your task is to carefully analyze the expressions given, and use the information from them to translate some new statements. 
    All of the information you need to do this task can be obtained from the given expressions. 

    Given the above expressions, please translate the following statements:
     a) from English into {language}

     b) from {language} into English. 

    -----------

    
    Chain of Thought with Self-Consistency (CoT-SC, as mentioned in Yao et al., style taken from promptingguide.ai/techniques/consistency)

    This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    Your task is to carefully analyze the expressions given, and use the information from them to translate some new expressions. 
    All of the information you need to do this task can be obtained from the given expressions. 
    
    Let's think through this carefully step by step, using logical reasoning to infer the meanings of the words and get the correct answer. 
    


    Given the above expressions, please translate the following statements:
     a) from English into {language}

     b) from {language} into English. 

    -----------

    STRESS



    Problem subtypes:

    Morphology
    Multilingual phonology transforms
    Stress patterns

    --> probably need a different prompt style for each one



    Base prompt: 

    This is a linguistics puzzle. Below are some words in {language} and their translations in English. 
    Your task is to carefully analyze the words given, and come up with rules to explain why some syllables in the word are stressed (corresponding to a 1) and the rest
    are unstressed. You will then apply your rules to infer the stress pattern of 0s and 1s in some new words. 

    [Some parts of the word are stressed

    HINT: Each word is made up of individual sound units called phonemes.]

    {data}

    Given the above expressions, please translate the following statements:
     a) from English into {language}

     b) from {language} into English. 

    '''
    #antara notes

    '''
    puzzling 

       [Here is an example: if <phrase 1> means <English phrase 1> anfrom huggingface_hub import login
login(token="your_access_token")d <phrase 2> means <English phrase 2, only 1 difference>, then 
    <the same thing> means <the shared meaning> 


    IDEA: we could see whether varying the example we provide it changes performance? Like if the example has an infix and the problem has an infix,
    does the example work as the hint to make the model look for that]

    saujas 

    LMAO ok the stress dataset has stress marked per character not per syllable....................is there a way we can change this T.T
    i think it might be helpful if we're testing something independent of program synthesis 

    [meta-comment: is there a way to flag when stress is purely phonological vs. if there is some semantic correlation as well? do we know that abt the dataset]

    '''
    #testing with data contamination 
    ''''
    This is a linguistics puzzle. You need to translate a sentence from english to {language} or vice verca.

    please translate the following statements:
     a) from English into {language}
    {eng}

     b) from {language} into English. 
    {lang}
     
    '''

    # for item in data['test']:
    #     eng_to_lang = ""
    #     lang_to_eng = ""
    #     if item[2] == "<":
    #         eng_to_lang += item[0] + "\n"
    #     else:
    #         lang_to_eng += item[1] + "\n"
        # call prompt DETECTION>"
        
        # "<PROMPT 2 FOR LINGUISTICS OLYMPIAD PROBLEM HERE>",
        # "<PROMPT FOR DATA CONTAMINATION - PRIOR PROBLEM DETECTION>",
        # "<PROMPT FOR DATA CONTAMINATION - PRIOR KNOWLEDGEurce += item[0] + '\n'"
        #     target += item[1] + "\n"
        #     source_and_target += item[0] + "\t" + item[1] + "\n"
        #     # print(source_and_target, source, target, source_language, target_language, meta)


    #we should probably change the temperature to 0.7 i think 
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

    #list of supported LLMs: https://docs.vllm.ai/en/latest/models/supported_models.html#supported-models

    # Added dummy support to skip LLM function calls
    if bool_use_LLM == True:
        llm = LLM(model = model_name)
        outputs = llm.generate(prompts, sampling_params)
    else:
        outputs = ['output01', 'output02', 'output03']

    # Deal with each output, then create
    # "outputs_[time_stamp]\[prompt_name]\[4-digit tag]_[target_language].txt"
    # Example: "outputs_19_22_37_06_05/base_prompt_puzzling/438d_turkish.txt"
    for idx, output in enumerate(outputs):
        prompt_name = prompt_names[idx]

        if bool_use_LLM == True:
            prompt = output.prompt
            generated_text = output.outputs[0].text
        else: 
            prompt = "dummy_prompt_content"
            generated_text = output

        # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

        # prepare the new path
        os.makedirs(os.path.join(path_out, prompt_name), exist_ok=True)
        source_lang_str = source_language.rstrip().replace(" ", "_")
        out_filename = os.path.join(path_out, prompt_name, f'{json_tag}_{source_lang_str}.txt')
        
        # TODO:
        with open(out_filename, "a+") as f:
            # f.append(generated_text)
            f.write(generated_text + "\n")
            print(f"SUCCESS: {out_filename} is saved.")
    
    print('\n')

    # for GPT 3.5 and 4: adding in the openAI API query stuff
    

    #TODO: ask for an api key lol 
    # openai_api_key = "037155e1b16a432fa836637370eca0e3"
    # openai_api_base = "http://localhost:8000/v1"

    # client = OpenAI(
    #     api_key=openai_api_key,
    #     base_url=openai_api_base,
    # )

    # chat_response = client.chat.completions.create(
    #     model=model_name,
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."}, # i wonder if we should change this to "you are a linguistics puzzle solver" or sth
    #         {"role": "user", "content": "Tell me a joke."},
    #     ]
    # )
    # print("Chat response:", chat_response)
            

# Populate some prompt templates, then return
# - prompt_names: A list of prompt names (such as "base_prompt_puzzling", "longer_prompt_puzzling", etc.)
# - prompts: A list of format strings of the populated templates
def create_puzzling_prompt(language, data, eng_to_lang, lang_to_eng):
    #-----------------------------------
    base_prompt_puzzling = f"""This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    {data}

    Given the above expressions, please translate the following statements:
    a) from English into {language}
    {eng_to_lang}

    b) from {language} into English.
    {lang_to_eng}""".format(language, data, eng_to_lang, lang_to_eng)
    
    #-----------------------------------
    
    longer_prompt_puzzling = f"""This is a linguistics puzzle. Below are some expressions in {language} and their English translations. 
    Your task is to carefully analyze the expressions given, and use the information from them to translate some new statements. 
    All of the information you need to do this task can be obtained from the given expressions. 

    {data}

    Given the above expressions, please translate the following statements:
     a) from English into {language}
     {eng_to_lang}

     b) from {language} into English.
     {lang_to_eng}""".format(language, data, eng_to_lang, lang_to_eng)
     
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
     {lang_to_eng}""".format(language, data, eng_to_lang, lang_to_eng)
    
    # [Manual Input]
    prompt_names = ['base_prompt_puzzling', 'longer_prompt_puzzling', 'cot_prompt_puzzling']
    prompts = [base_prompt_puzzling,
               longer_prompt_puzzling,
               cot_prompt_puzzling]
    
    return prompt_names, prompts
        

def use_gpt(prompts, model_name):
    """""""""
    formatting: "gpt35turbo" or "gpt4" as string
    """

    for prompt in prompts:
        client = AzureOpenAI(
                        azure_endpoint = "https://cullmsouthindia.openai.azure.com/", 
                        api_key="037155e1b16a432fa836637370eca0e3",  
                        api_version="2024-02-15-preview"
                    )
        message_text = [{"role":"system","content":""}, {"role":"user", "content": prompt}]

        completion = client.chat.completions.create(
                model=model_name, # model = "deployment_name"
                messages = message_text,
                temperature=0, #TODO: change to 0.8 to be consistent? -a
                max_tokens=20,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
        )
    return completion


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
    directory = path_for_data
    
    def download_and_extract_zip(url, directory):
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful

        # Create a ZipFile object from the response content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(directory)

    def get_first_four_chars(filename):
        if '/' in filename:
            # Split by slash and get last element (filename)
            first_four_chars = filename.split("/")[-1][:4]
        else:
            # No slash, assume entire string is filename/extension
            first_four_chars = filename[:4]
        return first_four_chars

    def read_puzzling_dataset(directory="None"):
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
        json_tags = []
        json_contents = []

        for file in json_files:
            file_path = os.path.join(directory, file)
            json_tag = get_first_four_chars(file_path)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                json_tags.append(json_tag)
                json_contents.append(data)

        return json_tags, json_contents

    # Download and extract the zip file
    download_and_extract_zip(url, path_for_data)

    # this has all the problems
    puzzling_problem_tags, puzzling_problem_set = read_puzzling_dataset(directory)
    return puzzling_problem_tags, puzzling_problem_set


def feed_problems_to_LLM(puzzling_problem_tags, puzzling_problem_set, model_name):
    # "data" is one .json file (one question)
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
                eng_to_lang += item[0] + "\n"
            else:
                lang_to_eng += item[1] + "\n"
                
        # prompts = create_puzzling_prompt(language=source_language, data=source_and_target, eng_to_lang=eng_to_lang, lang_to_eng=lang_to_eng)
        json_tag = puzzling_problem_tags[idx]
        prompt_names, prompts = create_puzzling_prompt(language=source_language, data=source_and_target, eng_to_lang=eng_to_lang, lang_to_eng=lang_to_eng)
        
        # use_gpt(prompts, "gpt4")
        # [CAUTION] Inside of "use_vllm()", bool_use_LLM would implement dummy if needed.
        use_vllm(json_tag, source_language, prompt_names, prompts, model_name)
      
        # call prompt


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


# [?] What kind of input are we expecting?
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

        # Example output
        # print(f"Source Language: {source_language}")
        # print(f"Target Language: {target_language}")
        # print(f"Meta: {meta}")
        # print(f"Source and Target:\n{source_and_target}")

# Initialize and transform the dataset
# problems = init_phonological_generalizations_data()
# transformed_data = transform_data(problems)

# # Load the transformed data
# phonological_generalizations_data_loader(transformed_data)

def main():

    model_name_llama = 'meta-llama/Meta-Llama-3-70B-Instruct'

    puzzling_data_tags, puzzling_problem_set = init_puzzling_data()
    feed_problems_to_LLM(puzzling_data_tags, puzzling_problem_set, model_name_llama)
    
    # model = "mistralai/Mistral-7B-v0.1"
    # use_vllm(model)
    
    
if __name__ == "__main__":
    main()
    
