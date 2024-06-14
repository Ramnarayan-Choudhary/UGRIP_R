'''
multiing_llm_eval.py

UGRIP Linguistics Olympiad Project
Updated 06/13/2024 @21:20 PM by Huanying (Joy) Yeh

Content:
- Main evaluation script of LLM response performance on the PuzzLing dataset 

Dependencies: "puzzling_eval_modules/evaluate.py", "util.py"

Input: 
- "LLM_raw_answers/{source_lang}_RAW_ANSWERS/{target_lang}" folder all LLM source_langs's answrs, 
    sub-directories are target_langs
- list_of_source_langs: list of LLM source_langs to evaluate
- list_of_target_langs: list of target_langs to evaluate
- bool_edit_json_names: whether to edit the json names into 
  [4-digit]_[source_lang]_[target_lang].json
- colors_all: list of colors for each source_lang and target_lang
- test_bench_dir = 'LLM_eval_test_bench' (this has to have all the ground truths 
  in the "ref" folder)

Output folders:
- 'LLM_eval_results': 
    -- "all_LLMS_scores_summary.csv"
    -- "{source_lang}_{target_lang}_scores.csv"
- 'LLM_eval_figures_by_source_lang' 
- 'LLM_eval_figures_all'


- 'LLM_multilingual_target_eval_results\{source_lang}_multilingual_scores.csv"
    - ['target_lang', 'source_lang', 'dist_to_eng', 'dist_to_source', 'CHRF', 'BLEU'...]

- 'LLM_multilingual_target_eval_figures':
    - '{source_lang}_multilingual_surf_plot.png'
    

'''

import os
import subprocess
import time
from util_eval_puzzling import *
import matplotlib.pyplot as plt
import numpy as np

# -------------- STEP 0: Config -----------------------
# Loop through all source_langs
# list_of_source_langs = ['madak', 'dyirbal', 'wambaya', 'yonggom']
# list_of_target_langs = ['english', 'dutch', 'estonian']

list_of_source_langs = ['madak']
list_of_target_langs = ['english']

# Don't modify these
start_time = time.time()

test_bench_dir = 'GPT4_global_eval_test_bench'
output_dir_temp = 'GPT4_global_eval_results_temp'
output_dir_actual = 'GPT4_global_eval_results'
fig_out_dir_indiv = 'GPT4_global_eval_figures_by_source_lang'
fig_out_dir_all = 'GPT4_global_eval_figures_all'

os.makedirs(test_bench_dir, exist_ok=True)
os.makedirs(os.path.join(test_bench_dir, 'res'), exist_ok=True)

os.makedirs(output_dir_temp, exist_ok=True)
os.makedirs(output_dir_actual, exist_ok=True)
os.makedirs(fig_out_dir_indiv, exist_ok=True)
os.makedirs(fig_out_dir_all, exist_ok=True)

all_source_langs_csv_name = "GPT4_global_scores_summary.csv"
all_source_langs_plot_name = "GPT4_global_scores_plot.png"

# Variable to enforce running the evaluation regardless of existing files
bool_enforce_running = False  # Set this to True or False as needed

# Set up the target directory of global IOL

colors_per_problem = {
    "chickasaw": "#8bff8b",  # easy
    "norwegian": "#00f800",  # easy
    "euskara": "#00d300",    # easy
    "blackfoot": "#ffb76f",  # medium
    "luise00o": "#ff8a4f",   # medium
    "basque": "#ff5219",     # medium
    "madak": "#00f800",      # hard (slightly brighter purple, switched -antara)
    "wambaya": "#ca68ca",    # hard (bright purple)
    "dyirbal": "#800080",    # hard (medium purple)
    "yonggom": "#ff8a4f",    # hard (dark purple)
    "overall": "#0000FF"     # Average
}

# Define colormaps
colors_all = [
    '#0000FF', '#5F9EA0', '#ADD8E6',  # Dark, medium, light blue GPT-4
    '#008000', '#32CD32', '#90EE90',  # Dark, medium, light green LLAMA-3
    '#FF8C00', '#FFA500', '#FFD700',  # Dark, medium, light orange MISTRAL
    '#8B008B', '#FF00FF', '#FF77FF',  # Dark, medium, light magenta GPT-35
    '#4B0082',  '#800080', '#DA70D6'  # Light Purple LLAMA-70B
    ]

if not bool_enforce_running and all_eval_report_exist(output_dir_actual, list_of_source_langs, list_of_target_langs):
    print("NOTE: all source_langs evaluation already exists. Skipping...")
else:
    print("NOTE: evaluating source_langs...")

# Gennerate the .txt 
for source_lang in list_of_source_langs: # madak
    for target_lang in list_of_target_langs: # english

        if bool_enforce_running or not this_eval_report_exists(output_dir_actual, source_lang, target_lang):
            print(f"NOTE: evaluating {source_lang} {target_lang}...")

            # ------------ STEP 01: COPY LLM ANSWER INTO TEST BENCH -----------------
            filename = f'{source_lang}_{target_lang}_answers.json'
            llm_source_dir = f'multiling_llm_answers/{source_lang}'
            
            shutil.copyfile(os.path.join(llm_source_dir, filename), 
                            os.path.join(test_bench_dir, 'res', filename))

            # ----------- STEP 02: Call the evaluation script -----------------------
            evaluate_script_path = 'puzzling_eval_modules/evaluate.py'

            # python3 'puzzling_eval_modules/evaluate.py' 'GPT4_global_eval_test_bench' 'GPT4_global_eval_results_temp' 'madak' 'english'
            command = ["python3", evaluate_script_path, test_bench_dir, output_dir_temp, source_lang, target_lang]
            msg = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            print(msg.stdout, end='\n')

        else:
            print(f"NOTE: {source_lang} {target_lang} evaluation already exists. Skipping...")

# ----------- STEP 03: Save to .csv ------------------------------------
status, df = create_eval_csv_global(output_dir_temp, output_dir_actual)
print(status)

# ----------- STEP 04: Save figs for each source_lang ------------------------
status = create_scores_plot_indiv(df, fig_out_dir_indiv, source_lang, target_lang, colors_per_problem)
status = create_scores_bars_indiv(df, fig_out_dir_indiv, source_lang, target_lang, colors_per_problem)
print(status + '\n')

status = create_scores_plot_all(df, fig_out_dir_all, colors_all, all_source_langs_plot_name)
print(status)

status = create_scores_bars_all(df, fig_out_dir_all)
print(status)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"SUCCESS: Evaluation completed. Total time: {elapsed_time:.3f} seconds.")
