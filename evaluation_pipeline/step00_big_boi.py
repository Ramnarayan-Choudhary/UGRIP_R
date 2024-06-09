'''
Step00_streamlined_LLM_data.py

UGRIP Linguistics Olympiad Project
Updated 06/07/2024 @12:40 PM by Huanying (Joy) Yeh

Content:
- Take in a directory with many "[4-digit tag]_[target_language]_scores.txt" file saved from step 01
- Parses the .txt file
- Saves the output visualizations
'''

import os
import shutil
import json
import re
import subprocess
from util import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

current_directory = os.getcwd()

# -------------- STEP 0: Config -----------------------
# Loop through all models
experiment_name_prefix = '06-09_PuzzLing_10_Problems'
list_of_models = ['GPT_35_TURBO', 'GPT_4', 'LLAMA_3', 'LLAMA_70B','MISTRAL']
list_of_prompts = ['BASIC', 'LONGER', 'COT']
bool_edit_json_names = [False, True, False, False, False]

llm_target_dir = 'LLM_eval_test_bench'
output_dir_actual = 'LLM_eval_results'

fig_out_dir_indiv = 'LLM_eval_figures_by_model'
fig_out_dir_all = 'LLM_eval_figures_all'

all_models_csv_name = "all_LLMs_scores_summary.csv"

os.makedirs(llm_target_dir, exist_ok=True)
os.makedirs(output_dir_actual, exist_ok=True)
os.makedirs(fig_out_dir_indiv, exist_ok=True)
os.makedirs(fig_out_dir_all, exist_ok=True)

# Implement file existence pre-check
if not all_eval_report_exist(output_dir_actual, list_of_models, list_of_prompts):
    print("NOTE: evaluating models...")
    for model in list_of_models:
        for prompt in list_of_prompts:
            if not this_eval_report_exists(output_dir_actual, model, prompt):
                print(f"NOTE: evaluating {model} {prompt}...")
                # ------------ STEP 01: COPY AND RENAME JSON FILES -----------------
                llm_source_dir = f'LLM_raw_answers/{model}_RAW_ANSWERS/{prompt}'
                bool_edit_json_name = bool_edit_json_names[list_of_models.index(model)]
                status = setup_test_bench(llm_source_dir, llm_target_dir, bool_edit_json_name)
                print(status)

                # ----------- STEP02: Call the evaluation script -----------------------
                evaluate_script_path = "data_evaluation_script/evaluate.py"
                output_dir_temp = f'LLM_eval_results_temp'
                os.makedirs(output_dir_temp, exist_ok=True) 
                command = ["python3", evaluate_script_path, llm_target_dir, 
                        output_dir_temp, model, prompt]

                msg=subprocess.run(command, capture_output=True, text=True)
                print(f"SUCCESS: Command executed: {' '.join(command)}")
                print(msg.stdout, end='')

                # ----------- STEP03: Save to .csv ------------------------------------
                # Init regex patterns
                status, df = create_eval_csv(output_dir_temp, output_dir_actual, model, prompt)
                print(status)

                # ----------- STEP04: Save figs for each model ------------------------
                status = create_scores_plot_indiv(df, fig_out_dir_indiv, model, prompt)
                print(status)
            else:
                print(f"NOTE: {model} {prompt} evaluation already exists. Skipping...")
else:
    print("NOTE: all models evaluation already exists. Skipping...")

# ----------- STEP05: Make excel report for all models ------------------------
status, df = create_all_models_eval_csv(output_dir_actual, list_of_models, 
                                    list_of_prompts, all_models_csv_name)
print(status)

status = create_scores_plot_all(df, fig_out_dir_all)
print(status)