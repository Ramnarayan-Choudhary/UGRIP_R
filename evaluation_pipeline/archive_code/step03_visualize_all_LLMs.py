'''
Step03_overall_scores_compare.py

UGRIP Linguistics Olympiad Project
Updated 06/07/2024 @12:40 PM by Huanying (Joy) Yeh

Content:
- Take in a directory with many "[4-digit tag]_[target_language]_scores.txt" file saved from step 01
- Parses the .txt file
- Saves the output visualizations

Notes: 
- Link to evaluation scripts: https://ukplab.github.io/PuzzLing-Machines/
'''
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np


# 1. Specify target directory (using raw string to avoid unicode escape issues)
root_path = 'C:/Users/joy20/Folder/SU_2024/UGRIP'
eval_general_path = 'all_data_copy'

# Put this new plot in a new folder
out_path = os.path.join(root_path, 'all_data_plots')
os.makedirs(out_path, exist_ok=True)

# This loops through 9 things
list_of_models = ['GPT_4', 'LLAMA_3', 'MISTRAL', 'GPT_35_TURBO', 'LLAMA_70B']

# list_of_models = ['LLAMA_3', 'LLAMA_70B', 'MISTRAL']
list_of_prompts = ['BASIC', 'LONGER', 'COT']

# list_of_models = ['GPT_4','GPT_35_TURBO']
# list_of_prompts = ['BASIC', 'LONGER', 'COT']

out_csv_name = 'all_models_scores_summary_temp.csv'
out_fig_name = 'models_compare_GPT_35_vs_GPT_4.png'
title_text = f"GPT_35_Turbo vs. GPT_4 Avg. Scores (10 R.S. Proplems)"


colors = [
    '#0000FF', '#5F9EA0', '#ADD8E6',  # Dark, medium, light blue
    '#8B008B', '#FF00FF', '#FF77FF',   # Dark, medium, light magenta
]

# colors = [
#     '#008000', '#32CD32', '#90EE90',  # Dark, medium, light green
#     '#B8860B',  # Dark Goldenrod
#     '#DAA520',  # Goldenrod
#     '#FFD700',  # Gold
    
# ]

# 12 colors total
colors_all = [
    '#0000FF', '#5F9EA0', '#ADD8E6',  # Dark, medium, light blue GPT-4
    '#008000', '#32CD32', '#90EE90',  # Dark, medium, light green LLAMA-3
    '#FF8C00', '#FFA500', '#FFD700',  # Dark, medium, light orange MISTRAL
    '#8B008B', '#FF00FF', '#FF77FF',   # Dark, medium, light magenta GPT-35
    '#4B0082',  '#800080', '#DA70D6' # Light Purple LLAMA-70B
    ]

# Init regex patterns
data_frames = []
score_pattern = re.compile(r'(\w+_SCORE):\s*(\d+\.\d+)')

# Loop through 9 things
for model in list_of_models:
    for prompt in list_of_prompts:
        target_dir = os.path.join(root_path, eval_general_path)
        # 2. Loop through each file in the directory
        for filename in os.listdir(target_dir):
            if filename.endswith(f"{model}_{prompt}_overall_scores.txt"):
                file_path = os.path.join(target_dir, filename)
    
                # Read the content of the file
                with open(file_path, 'r') as file:
                    content = file.read()
                
                # Extract the scores from the content
                scores = score_pattern.findall(content)
                score_dict = {score[0]: float(score[1]) for score in scores}

                score_dict['model'] = model
                score_dict['prompt'] = prompt

                # Convert the dictionary to a DataFrame and append it to the list
                data_frames.append(pd.DataFrame([score_dict]))

        # 3. Generate the dataframe
        df = pd.concat(data_frames, ignore_index=True)
        columns_order = ['model', 'prompt'] + [col for col in df.columns if col not in ['model', 'prompt']]
        df = df[columns_order]

        # 4. save the DataFrame to a CSV file
        df.to_csv(os.path.join(out_path, out_csv_name), index=False)
      
skip = False

if not skip:
    # Define the columns for the x-axis (score fields)
    score_fields = np.array([col for col in df.columns if col not in ['model', 'prompt']])

    # Define the y-axis (accuracy, assuming scores are percentages)
    accuracy = df[score_fields]

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot scatter points for each problem (each row in the DataFrame)
    for i in range(len(df)):
        x = np.arange(len(score_fields))  # Generate x values as indices for score fields
        y = accuracy.iloc[i].values  # Select accuracy values for the current row
        
        # Scatter plot with random jitter on the x-axis for better visualization
        # ax.plot(x + np.random.normal(0, 0.05, len(x)), y, 
        #         label=f"{df['tag'][i]}_{df['target_lang'][i]}", linewidth=2.5)

        ax.plot(x, y, label=f"{df['model'][i]}_{df['prompt'][i]}", linewidth=2.5, color=colors[i])

    # Set labels and title
    ax.set_ylim([0, 110])
    ax.set_xlabel('Score Fields')
    ax.set_ylabel('Accuracy (%)')

    ax.set_title(title_text)

    # Set x-axis tick labels to score field names
    plt.xticks(np.arange(len(score_fields)), score_fields, rotation=45, ha='right')

    # Add legend and grid
    ax.legend(title='Legend', bbox_to_anchor=(1, 1), ncol=1)

    ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.savefig(os.path.join(out_path, out_fig_name))
    plt.show()
