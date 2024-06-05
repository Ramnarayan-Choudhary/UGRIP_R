# test 
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from transformers import pipeline
import torch
import requests
import zipfile
import io
import os
import json
from vllm import LLM, SamplingParams
from openai import OpenAI, AzureOpenAI
from huggingface_hub import login


login(token="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")

# prompt func

# --------

m = "mistralai/Mistral-7B-v0.1"



# setting up VLLM

# installed VLLM, OpenAI etc. packages on my conda UGRIP envt! 



# Set OpenAI's API key and API base to use vLLM's API server.
# so does this work for all of the available LLM? like the syntax n stuff is the same? Ok than it makes thing easier then 

#yup looks like! we just have to change the model name 
# so im just writing as a function so we dont have to make a separate instance each time
# hehehe yes it does make life easy


def use_vllm(prompts, model_name):
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

    # so does this work for all of the available LLM?

    # im moving the load model outside
    # yup ok

    llm = LLM(model = model_name)

    outputs = llm.generate(prompts, sampling_params)


    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

        # TODO:
        with open("output.txt", "a+") as f:
            f.append(generated_text)

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
    
    prompts = [base_prompt_puzzling,
               longer_prompt_puzzling,
               cot_prompt_puzzling]
    
    return prompts
        

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




def init_puzzling_data(directory="None"):
    '''
    dataset format:
    a list of :
    'source_language'
    'target_language'
    'meta'
    'train' : a pair of source and target in a list
    'test' : a pair of source and target in a list (one is empty)
    '''
    url = 'https://ukplab.github.io/PuzzLing-Machines/data/public_data_test.zip'
    # Directory where the contents will be extracted
    if directory ==  "None":
        directory = os.getcwd()  # Current directory

    def download_and_extract_zip(url, directory="None"):
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful

        # Create a ZipFile object from the response content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # Extract all the contents into the specified directory
            zip_ref.extractall(directory)

    def read_puzzling_dataset(directory="None"):
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
        json_contents = []

        for file in json_files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'r') as f:
                data = json.load(f)
                json_contents.append(data)

        return json_contents

    # Download and extract the zip file
    download_and_extract_zip(url, directory)
    puzzling_data = read_puzzling_dataset(directory)
    return puzzling_data

def puzzling_data_loader(puzzling_data):
    for data in puzzling_data:
        # 
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
            # print(source_and_target, source, target, source_language, target_language, meta)
            
        eng_to_lang = ""
        lang_to_eng = ""
            
        for item in data['test']:
            
            if item[2] == "<":
                eng_to_lang += item[0] + "\n"
            else:
                lang_to_eng += item[1] + "\n"
                
        prompts = create_puzzling_prompt(language=source_language, data=source_and_target, eng_to_lang=eng_to_lang, lang_to_eng=lang_to_eng)
        # use_gpt(prompts, "gpt4")
        use_vllm(prompts, 'meta-llama/Meta-Llama-3-70B-Instruct')
        # call prompt
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
    puzzling_problem = init_puzzling_data()
    puzzling_data_loader(puzzling_problem)
    # model = "mistralai/Mistral-7B-v0.1"
    # use_vllm(model)
    
    
if __name__ == "__main__":
    main()
    