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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_scores_bars_indiv_BLEU_EM(df, fig_out_dir, model, prompt):
    # Select target languages and their respective scores (excluding 'overall')
    out_filename = f'BLEU_EM_contam_score_bar_{model}_{prompt}.png' # CHANGE THIS

    target_langs = df['target_lang'][:-1]
    BLEU_SCORE = df['BLEU_SCORE'][:-1]
    EM_SCORE = df['EM_SCORE'][:-1]
    contaminate = df['Contamination']
    
    # Set the width of the bars
    bar_width = 0.4
    
    # Set the positions of the bars on the x-axis
    r1 = np.arange(len(target_langs))
    r2 = [x + bar_width for x in r1]
    
    # Define colors
    colors = {
        'red1': '#a60000',
        'red2': '#ed0000',
        'green1': '#1b751a',
        'green2': '#18bc22'
    }
    # Create the bar plot
    plt.figure(figsize=(21, 10.5))
    
    for i in range(len(target_langs)):
   
        tag = contaminate[i]
        tag = tag.replace(" ", "")
     
        color1 = colors['red1'] if (tag == 'yes') else colors['green1']
        color2 = colors['red2'] if (tag == 'yes') else colors['green2']
        
        plt.bar(r1[i], BLEU_SCORE[i], color=color1, width=bar_width, edgecolor='grey')
        plt.bar(r2[i], EM_SCORE[i], color=color2, width=bar_width, edgecolor='grey')
       
    # Add xticks on the middle of the group bars
    plt.xlabel('Target Language', fontweight='bold', fontsize=18)
    plt.xticks([r + bar_width for r in range(len(target_langs))], target_langs, rotation=45)
    # plt.xticks([r + bar_width for r in range(12)], target_langs, rotation=45)
    
    # Add labels and title
    plt.ylabel('Accuracy (%)', fontweight='bold',fontsize=18)
    plt.title(f'{model}_{prompt} PuzzLing Scores (BLEU and Exact Match Only)', fontweight='bold', fontsize=26)
    
    # Custom legend
    handles = [
        plt.Rectangle((0,0),1,1, color=colors['red1'], edgecolor='grey'),
        plt.Rectangle((0,0),1,1, color=colors['red2'], edgecolor='grey'),
    
        plt.Rectangle((0,0),1,1, color=colors['green1'], edgecolor='grey'),
        plt.Rectangle((0,0),1,1, color=colors['green2'], edgecolor='grey')
        
    ]
    labels = ['BLEU_SCORE (Contaminted)', 'EM_SCORE (Contaminated)', 
              'BLEU_SCORE (Good)', 'EM_SCORE (Good)']
    plt.legend(handles, labels)

    plt.tight_layout()
    try: 
        plt.savefig(os.path.join(fig_out_dir, out_filename))
        status = f"SUCCESS: created {out_filename}."
        return status
    
    except Exception as e:
        print(f"Error: {e}")

# -------------- STEP 0: Config -----------------------
# Loop through all models
list_of_models = ['GPT_35_TURBO', 'GPT_4', 'LLAMA_3_70B','MISTRAL']
list_of_prompts = ['BASIC', 'LONGER']
fig_out_dir_indiv = 'LLM_eval_figures_by_model'
os.makedirs(fig_out_dir_indiv, exist_ok=True)

for model in ['GPT_4', 'GPT_35_TURBO', 'LLAMA_3_70B', 'MISTRAL']:
    for prompt in ['BASIC', 'LONGER']:
        # Read this model's csv file
        csv_file = f'LLM_eval_results_with_contamination_data/{model}_{prompt}_scores_summary_with_contam.csv'
        df = pd.read_csv(csv_file)  
        status = create_scores_bars_indiv_BLEU_EM(df, fig_out_dir_indiv, model, prompt)
        print(status + '\n')

print(f"SUCCESS: Evaluation completed.")
