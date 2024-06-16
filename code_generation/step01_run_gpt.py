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
import time

max_tokens = 500
input_prompt_path = 'input_prompts'
out_convos_path = 'output_convos'

os.makedirs(input_prompt_path, exist_ok=True)
os.makedirs(out_convos_path, exist_ok=True)

# Prepare the prompt

topic = '01_language_creation'
prompt_filename = f"{topic}.txt"
all_prompts_txt = os.path.join(input_prompt_path, prompt_filename)

print(f"\nSUCCESS: {all_prompts_txt} saved.\n")

# Run GPT
model_name = 'gpt4'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
start_time = time.time()

client = gpt.load_model(model_name)
prompts = gpt.read_convo_from_file(all_prompts_txt)
response_dict, responses = gpt.process_prompts(prompts, client, model_name, max_tokens)

end_time = time.time()
runtime = f'{(end_time - start_time):.3f}'

gpt.save_convo_to_txt(all_prompts_txt, topic, 
                      responses, timestamp, model_name, runtime, topic)
gpt.save_convo_to_json(response_dict, topic, timestamp)  

print('\nSUCCESS: All tasks completed successfully.')
