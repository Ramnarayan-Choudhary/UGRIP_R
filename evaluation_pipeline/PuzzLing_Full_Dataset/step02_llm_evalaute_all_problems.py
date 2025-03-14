'''
llm_evaluate.py

UGRIP Linguistics Olympiad Project
Updated 06/10/2024 @11:20 AM by Huanying (Joy) Yeh

Content:
- Main evaluation script of LLM response performance on the PuzzLing dataset 

Dependencies: "puzzling_eval_modules/evaluate.py", "util.py"

Input: 
- "LLM_raw_answers/{model}_RAW_ANSWERS/{prompt}" folder all LLM models's answrs, 
    sub-directories are prompts
- list_of_models: list of LLM models to evaluate
- list_of_prompts: list of prompts to evaluate
- bool_edit_json_names: whether to edit the json names into 
  [4-digit]_[model]_[prompt].json
- colors_all: list of colors for each model and prompt
- llm_target_dir = 'LLM_eval_test_bench' (this has to have all the ground truths 
  in the "ref" folder)

Output folders:
- 'LLM_eval_results': 
    -- "all_LLMS_scores_summary.csv"
    -- "{model}_{prompt}_scores.csv"
- 'LLM_eval_figures_by_model' 
- 'LLM_eval_figures_all'

'''

import os
import subprocess
import time
from util import *
import matplotlib.pyplot as plt
import numpy as np

# -------------- STEP 0: Config -----------------------
# Loop through all models
list_of_models = ['GPT_35_TURBO', 'GPT_4', 'LLAMA_3_70B','MISTRAL']
list_of_prompts = ['BASIC', 'LONGER']

# list_of_models = ['MISTRAL']
# list_of_prompts = ['LONGER']

bool_edit_json_names = [False, False, False, False]

colors_all = [
    '#0000FF', '#5F9EA0',  # Dark, medium, light blue GPT-35-Turbo
    '#008000', '#32CD32',  # Dark, medium, light green GPT-4
    '#FF8C00', '#FFA500',  # Dark, medium, light orange MISTRAL
    '#8B008B', '#FF00FF',  # Dark, medium, light magenta llama-3-70B
    # '#4B0082',  '#800080', '#DA70D6'  # Light Purple LLAMA-70B
    ]


# colors_per_problem = {
#     "chickasaw": "#8bff8b",  # easy
#     "norwegian": "#00f800",  # easy
#     "euskara": "#00d300",    # easy
#     "blackfoot": "#ffb76f",  # medium
#     "luise00o": "#ff8a4f",   # medium
#     "basque": "#ff5219",     # medium
#     "madak": "#e898c6",      # hard (slightly brighter purple, switched -antara)
#     "wambaya": "#ca68ca",    # hard (bright purple)
#     "dyirbal": "#800080",    # hard (medium purple)
#     "yonggom": "#6100a9",    # hard (dark purple)
#     "average": "#0000FF"     # Average
# }

# Define colormaps
# colors_all = [
#     '#0000FF', '#5F9EA0', '#ADD8E6',  # Dark, medium, light blue GPT-35-Turbo
#     '#008000', '#32CD32', '#90EE90',  # Dark, medium, light green GPT-4
#     '#FF8C00', '#FFA500', '#FFD700',  # Dark, medium, light orange MISTRAL
#     '#8B008B', '#FF00FF', '#FF77FF'  # Dark, medium, light magenta llama-3-70B
#     # '#4B0082',  '#800080', '#DA70D6'  # Light Purple LLAMA-70B
#     ]

# Don't modify these
start_time = time.time()

llm_target_dir = 'LLM_eval_test_bench'
output_dir_actual = 'LLM_eval_results'
fig_out_dir_indiv = 'LLM_eval_figures_by_model'
fig_out_dir_all = 'LLM_eval_figures_all'

all_models_csv_name = "all_LLMs_scores_summary.csv"
all_models_plot_name = "all_LLMs_scores_plot.png"

output_dir_temp = 'LLM_eval_results_temp'
os.makedirs(output_dir_temp, exist_ok=True) 

os.makedirs(llm_target_dir, exist_ok=True)
os.makedirs(output_dir_actual, exist_ok=True)
os.makedirs(fig_out_dir_indiv, exist_ok=True)
os.makedirs(fig_out_dir_all, exist_ok=True)

# Implement file existence pre-checkimport os
import subprocess

# Variable to enforce running the evaluation regardless of existing files
bool_enforce_running = True  # Set this to True or False as needed

if not bool_enforce_running and all_eval_report_exist(output_dir_actual, list_of_models, list_of_prompts):
    print("NOTE: all models evaluation already exists. Skipping...")
else:
    print("NOTE: evaluating models...")
    for model in list_of_models:
        for prompt in list_of_prompts:
            if bool_enforce_running or not this_eval_report_exists(output_dir_actual, model, prompt):
                print(f"NOTE: evaluating {model} {prompt}...")
                # ------------ STEP 01: COPY AND RENAME JSON FILES -----------------
                llm_source_dir = f'LLM_cleaned_answers/{model}/{prompt}'
                bool_edit_json_name = False
                status = setup_test_bench(llm_source_dir, llm_target_dir, False)
                print(status)

                # ----------- STEP 02: Call the evaluation script -----------------------
                evaluate_script_path = "puzzling_eval_modules/evaluate.py"
                
                os.makedirs(f'{llm_target_dir}/res', exist_ok=True)

                command = ["python3", evaluate_script_path, llm_target_dir, 
                           output_dir_temp, model, prompt]

                msg = subprocess.run(command, capture_output=True, text=True)
                print(msg.stdout, end='')

                # ----------- STEP 03: Save to .csv ------------------------------------
                # Init regex patterns
                status, df = create_eval_csv(output_dir_temp, output_dir_actual, model, prompt)
                print(status)

                # ----------- STEP 04: Save figs for each model ------------------------
                status = create_scores_plot_indiv(df, fig_out_dir_indiv, model, prompt)
                status = create_scores_bars_indiv(df, fig_out_dir_indiv, model, prompt)
                print(status + '\n')
            
            else:
                print(f"NOTE: {model} {prompt} evaluation already exists. Skipping...")


# ----------- STEP05: Make excel report and all_model plots ------------------------
status, df = create_all_models_eval_csv(output_dir_actual, list_of_models, list_of_prompts, all_models_csv_name)
print(status)

status = create_scores_plot_all(df, fig_out_dir_all, colors_all, all_models_plot_name)
print(status)

status = create_scores_bars_all(df, fig_out_dir_all)
print(status)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"SUCCESS: Evaluation completed. Total time: {elapsed_time:.3f} seconds.")
