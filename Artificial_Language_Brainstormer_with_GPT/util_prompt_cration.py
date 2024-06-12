# Utility functions for creating propmpts
# Format strings
# Reading the raw .json files

import json

def read_json_file_as_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_string = file.read()
    return json_string


def extract_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    source_language = data['source_language']
    target_language = data['target_language'] # default in english
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

    return source_language, target_language, source_and_target, eng_to_lang, lang_to_eng


# Tell GPT to solve the problem
def create_puzzling_prompt(json_problem_statement, json_test_template):

    base_prompt_puzzling = f"""
    1. This is a linguistics puzzle. The given pair of English to unknown language translations are as follows:
    Note that the translation pairs are written in json format.

    {json_problem_statement}

    2. Now, please complete the missing slots in the following "test" problem set, also in .json file.
    
    The following json is called "test_problem_set":

    {json_test_template}

    3. Here are some explanaions of the problem statement above:
    In the JSON file, you will see many lists of 3 elements
    Each list element would have two formats:

    Option 1: ["", "two languages", "<"]. The "<" means that the English translation is given.
    So you are supposed to translate "two languages", which is an English statement, into the unknwon language. 
    Then, fil in the answer at the first element in the list, "". 
    Do not change element 2 and 3, which are "two languages" and "<" respectively.

    Option 2: you might see ["ewriwurweir", "", ">"]. The ">" means that the translation in the unknown language is given. 
    Then you're supposed to fill in the English translation in the second element, at "". 
    The first element, "ewriwurweir", and the third element, ">", should not be changed.

    4. Go through all the 3-element lists, then answer the questions, depending on which way you see the ">" or "<".
    Only populate the missing "" in any given 3-element list. Do not modify the order of the list elements, either.
   
    5. Output the completed JSON, strictly follow the structure of the JSON template.
    Again, make sure that all the elements are in the same order as the "test_problem_set", with only the "" fields populated, whereever they may be.
    """

    return base_prompt_puzzling


# Format intot the chatbot API text file
# Make additional requests
def create_chatbot_prompt(prompt, json_test_template):
    formatted_prompt = f"""Conversation with GPT-3.5-turbo 
Time Stamp: 06-12-2024, 08:42 AM
Topic: Translating the Task

>>>> Prompt 1 >>>>
{prompt}
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

-----------------------------------------
[insert respone 1]
>>>>--------------------------------->>>>

>>>> Prompt 2 >>>>
Please look at your previous response, then compare line-by-line with the following template:

{json_test_template}

Make sure that your response is exacetly in the same format and sentence ordering.
If one element is in English, then the corresponding line should also be in English.
Same for the unknown language.
If any element order is swapped, please fix it so that the in any 3-element list, 
we always have [Unknown, English, < or >] in that order.
Please output the json again. No need to wrap it around "```json" and "```".
I just need the content.
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

>>>> Prompt 4 >>>>
Can you explain why you think that's the language?
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

-----------------------------------------
[insert respone 4]
>>>>--------------------------------->>>>
"""
    return formatted_prompt