# Big PuzzLing benchmark evaluation edited
# Format the Google Drive formatted JSON for eval
# Run this script before running llm_evaluate_all_data.py

import json
import os
import re
import itertools

# Step00: Uesr config
# list_of_models = ['GPT_35_TURBO', 'GPT_4', 'LLAMA_3_70B','MISTRAL']
# list_of_prompts = ['BASIC', 'LONGER']

list_of_models = ['MISTRAL']
list_of_prompts = ['LONGER']

# Config, don't change
raw_answers_path = 'LLM_raw_answers'
test_template_path = 'LLM_raw_problem_sets'
ref_path = 'LLM_eval_test_bench/ref'

out_path = 'LLM_cleaned_answers'
os.makedirs(out_path, exist_ok=True)

# Step01: Let GPT do the multilingual problems
for model in list_of_models: # madak
    for prompt in list_of_prompts: # english
        this_out_path = os.path.join(out_path, model, prompt)
        os.makedirs(this_out_path, exist_ok=True)

        # Load the test field of the json
        answers_path = os.path.join(raw_answers_path, f"{model}_RAW_ANSWERS", prompt)
                
        # Loop through JSON files in all the LLM answer keys
        for filename in os.listdir(answers_path):
            if filename.endswith('.json'):
                # Get the answer data
                filepath = os.path.join(answers_path, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    answer_data = json.load(file)

                # Get its matching raw exam set
                for test_filename in os.listdir(test_template_path):
                    if test_filename.startswith(filename[:4]):
                        target_filepath = os.path.join(test_template_path, test_filename)
                        test_data = json.load(open(target_filepath, 'r', encoding='utf-8'))
                        # print(test_filename)
                        break
                       
                new_ans_list = []
                
                test_data_copy = test_data
                # Fixing
                # Loop through both lists
                for ans, test in zip(answer_data['test'], test_data['test']):
                    new_ans = ans.copy()   # Make a copy of the ans or create a new list if ans is None
                    third_element = test[2]  # Get the third element of the test data

                    # Check if the answers are out of order, then fix it
                    if ans and ans[0] == test[1]:
                        new_ans[0] = ans[1]
                        new_ans[1] = ans[0]

                    # Check if the third element is ">" or "<"
                    if third_element == '<':
                        new_ans[1] = test[1]  # Populate the second element with the second element of the test data
                    elif third_element == '>':
                        new_ans[0] = test[0]  # Populate the first element with the second element of the test data

                    new_ans[2] = test[2]

                    new_ans_list.append(new_ans)

                # Append any remaining elements from test_data['test']
                if len(test_data['test']) > len(answer_data['test']):
                    for remaining_test in test_data['test'][len(answer_data['test']):]:
                        new_ans_list.append(remaining_test)



                test_data_copy['test'] = new_ans_list
                new_json_string = json.dumps(test_data_copy, indent=2, separators=(',', ':'), ensure_ascii=False)
               
                # Forced fix on maori
                # if filename.endswith('a8b1_m\xc4\x81ori.json'):
                
                if filename.endswith('a8b1_māori.json'):
                    if os.path.exists(os.path.join(out_path, model, prompt, filename)):
                        os.remove(os.path.join(out_path, model, prompt, filename))
                    filename = 'a8b1_maori.json'
        

                out_json_name = os.path.join(out_path, model, prompt, filename)

                with open(out_json_name, 'w', encoding='utf-8') as file:
                    file.write(new_json_string) 

                print(f"SUCCESS: {out_json_name} saved.")
            
                