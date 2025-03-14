# Utility functions for the multilingual experiment
# Format strings
# Reading the raw .json files

import json

def read_json_file_as_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_string = file.read()
    return json_string


def extract_json_content(file_path, source_lang, target_lang):
    
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Sanity check
    file_source_lang = json_data.get("source_language", "")
    file_target_lang = json_data.get("target_language", "")

    if file_source_lang != source_lang:
        print(f"Error: Source language mismatch. Expected {source_lang}, got {file_source_lang}.")
        return None
    if file_target_lang != target_lang:
        print(f"Error: Target language mismatch. Expected {target_lang}, got {file_target_lang}.")
        return None
    
    # Get JSON content
    
    train_content = '{"train": ' + json.dumps(json_data.get("train", []), indent=2, separators=(',', ':'), ensure_ascii=False) + '}'
    test_content = '{"test": ' + json.dumps(json_data.get("test", []), indent=2, separators=(',', ':'), ensure_ascii=False) + '}'
    
    return train_content, test_content


def create_longer_prompt(data, language, eng_to_lang, lang_to_eng):
    
    prompt = f"""This is a linguistics puzzle. Below are some expressions in the {language} language and their English translations. Your task is to carefully analyze the expressions given, and use the information from them to translate some new statements. This might involve logically reasoning about how words or parts of words are structured in {language}, what the word order could be, and how different grammatical phenomena could influence the expressions. 

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

    """

    return prompt


# Tell GPT to solve the problem
def create_puzzling_prompt(json_problem_statement, json_test_template, target_language):

    prompt = f"""1. This is a linguistics puzzle. The given pair of {target_language} to unknown language translations are as follows:
    Note that the translation pairs are written in json format.

    {json_problem_statement}

    2. Here, each pair of the problem statement gives you the unknown language and its respective translation in the target language. complete the missing slots in the following "test" problem set, also in .json file.
    
    The following json is called "test_problem_set":

    {json_test_template}

    3. Here are some explanaions of the problem statement above:
    In the JSON file, you will see many lists of 3 elements
    Each list element would have two formats:

    Option 1: ["", "two languages", "<"]. The "<" means that the {target_language} translation is given.
    So you are supposed to translate "two languages", which is an {target_language} statement, into the unknwon language. 
    Then, fil in the answer at the first element in the list, "". 
    Do not change element 2 and 3, which are "two languages" and "<" respectively.

    Option 2: you might see ["ewriwurweir", "", ">"]. The ">" means that the translation in the unknown language is given. 
    Then you're supposed to fill in the {target_language} translation in the second element, at "". 
    The first element, "ewriwurweir", and the third element, ">", should not be changed.

    4. Go through all the 3-element lists, then answer the questions, depending on which way you see the ">" or "<".
    Only populate the missing "" in any given 3-element list. Do not modify the order of the list elements, either.
   
    5. Output the completed JSON, strictly follow the structure of the JSON template.
    Again, make sure that all the elements are in the same order as the "test_problem_set", with only the "" fields populated, whereever they may be.
    """

    return prompt


# Format intot the chatbot API text file
# Make additional requests
def create_chatbot_prompt(prompt, json_test_template, source_lang, target_lang):
    formatted_prompt = f"""Conversation with GPT-4
Time Stamp: [insert timestamp]
Topic: Multilingual IOL translation. 
Source: {source_lang}. Target: {target_lang}

>>>> Prompt 1 >>>>
{prompt}
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

-----------------------------------------
[insert respone 1]
>>>>--------------------------------->>>>

>>>> Prompt 2 >>>>
Please look at your previous response, then compare line-by-line with the following template:

{json_test_template}

Make sure that your response is exacetly in the same format. 

In every 3-element sub-list in this json file, do the following.
If you see the third element being "<", then your use your translation result in the "unknown language" in the 1st element in the list, which replaces the "" placeholder.
If you see the third element being ">", then your use your translation result in {target_lang} in the 2nd element in the list, which replaces the "" placeholder.

Keep all elements that are already populated intact.

Please output the json again. No need to wrap it around "```json" and "```".

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

-----------------------------------------
[insert respone 2]
>>>>--------------------------------->>>>

>>>> Prompt 3 >>>>
What do you think this language is? Answer in one word, all lower case.
If you don't know, just type "unknown".
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

-----------------------------------------
[insert respone 3]
>>>>--------------------------------->>>>

"""
    return formatted_prompt