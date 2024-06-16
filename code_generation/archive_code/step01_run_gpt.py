# UGRIP IOL Problem
# Experiment: Translate to various "global soucre" languages and compare
# Apply distance metrics

# Updated 06/12/2024
# Sample language: Madak

'''
multilingual_target_language.py

UGRIP Linguistics Olympiad Project
Updated 06/12/2024 @10:00 AM by Huanying (Joy) Yeh

Content:
- Testing PuzzLing performances in various target languages, apart from English
- We call this the "global_target_lang"
- Evaluate and save reports to see whether 
    - the distance between "global_target_lang" and English matters more -> relying on meaning
    - the distance between "global_target_lang" and "source_lang" matters less -> relying on grammar structure

Dependencies: ???

Inputs:
- "multiling_problem_set/{source_lang}/{target_lsource_langang}_test.json" folder. Global target language tests
- "multiling_ref/{source_lang}/{target_lang}_ref.json" folder. Ground truths

- "multiling_llm_answers/{source_lang}/{target_lang}_answer.json" folder. The LLM responses, well-formatted. 

- llm_source_dir = 'LLM_eval_test_bench':
    - creates /ref from "global_lang_ref" 
    - creates /res from "llm_answers"

Outputs:
- output_report_filename = f'output_convos/{report_prefix}_GPT_convo.txt'
- json_filename = f"output_json/{report_prefix}_GPT_convo.json"

'''

import json
import os
import datetime
import util_gpt as gpt
import util_prompt_creation as prompting

# Step00: Uesr config
list_of_source_langs = ['dyirbal', 'wambaya', 'yonggom']
list_of_target_langs = ['english', 'dutch', 'estonian']

list_of_source_langs = ['dyirbal']
list_of_target_langs = ['english']

max_tokens = 500

# Config, don't change
input_prompt_path = 'input_prompts'
out_convos_path = 'output_convos'

os.makedirs(input_prompt_path, exist_ok=True)
os.makedirs(out_convos_path, exist_ok=True)


# Step01: Let GPT do the multilingual problems
for source_lang in list_of_source_langs: # madak
    for target_lang in list_of_target_langs: # english

        # Prepare the prompt
        input_exam_path = os.path.join("multiling_problem_set", 
                                       source_lang, f"{source_lang}_{target_lang}_test.json")
        train_content, test_content = prompting.extract_json_content(input_exam_path, source_lang, target_lang)
        prompt = prompting.create_puzzling_prompt(train_content, test_content, target_lang)
        formatted_prompt = prompting.create_chatbot_prompt(prompt, test_content, source_lang, target_lang)
       
        prompt_filename = f"{source_lang}_{target_lang}_prompt.txt"
        all_prompts_txt = os.path.join(input_prompt_path, prompt_filename)
        with open(all_prompts_txt, 'w', encoding='utf-8') as file:
            file.write(formatted_prompt)

        print(f"\nSUCCESS: {all_prompts_txt} saved.\n")

        # Run GPT
        timestamp = datetime.datetime.now().strftime("%H_%M_%S")
        client = gpt.load_model()
        prompts = gpt.read_convo_from_file(all_prompts_txt)
        response_dict, responses = gpt.process_prompts(prompts, client, max_tokens)
        
        report_prefix = f'{source_lang}_{target_lang}'
        gpt.save_convo_to_txt(all_prompts_txt, report_prefix, responses, timestamp)
        gpt.save_convo_to_json(response_dict, report_prefix, timestamp)  

    print('\nSUCCESS: All tasks completed successfully.')
