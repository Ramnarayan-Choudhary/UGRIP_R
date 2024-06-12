'''
Step02_eval_scores_visualize.py

UGRIP Linguistics Olympiad Project
Updated 06/06/2024 @16:00 PM by Huanying (Joy) Yeh

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

model = 'LLAMA_70B'
prompt = 'BASIC'

root_path = 'C:/Users/joy20/Folder/SU_2024/UGRIP'

# This loops through
# list_of_models = ['GPT_4', 'LLAMA_3', 'MISTRAL']
# list_of_prompts = ['BASIC', 'LONGER', 'COT']

# for model in list_of_models:
#     for prompt in list_of_prompts:
target_dir = f'{root_path}\{model}_{prompt}_EVAL'
target_out_dir = f'{root_path}\{model}_{prompt}_EVAL'
target_out_dupe_dir = 'all_data_copy'
os.makedirs(target_out_dupe_dir, exist_ok=True)

# Init regex patterns
data_frames = []
score_pattern = re.compile(r'(\w+_SCORE):\s*(\d+\.\d+)')

# 2. Loop through each file in the directory
for filename in os.listdir(target_dir):
    if filename.endswith("_scores.txt") and not filename.endswith("overall_scores.txt"):
        file_path = os.path.join(target_dir, filename)
        
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Extract the scores from the content
        scores = score_pattern.findall(content)
        score_dict = {score[0]: float(score[1]) for score in scores}

        # Extract tag and target language from filename
        tag, target_lang = filename.split('_')[:2]

        # Add tag and target language to the dictionary
        score_dict['tag'] = tag
        score_dict['target_lang'] = target_lang

        # Convert the dictionary to a DataFrame and append it to the list
        data_frames.append(pd.DataFrame([score_dict]))

# 3. Generate the dataframe
df = pd.concat(data_frames, ignore_index=True)
columns_order = ['tag', 'target_lang'] + [col for col in df.columns if col not in ['tag', 'target_lang']]
df = df[columns_order]

# 4. save the DataFrame to a CSV file
df.to_csv(os.path.join(target_out_dir, f'{model}_{prompt}_scores_summary.csv'), index=False)
df.to_csv(os.path.join(target_out_dupe_dir, f'{model}_{prompt}_scores_summary.csv'), index=False)

# 5.Work on plotting
import numpy as np
import matplotlib.pyplot as plt

# Define the columns for the x-axis (score fields)
score_fields = np.array([col for col in df.columns if col not in ['tag', 'target_lang']])

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

    ax.plot(x, y, label=f"{df['tag'][i]}_{df['target_lang'][i]}", linewidth=2.5)

# Set labels and title
ax.set_ylim([0, 110])
ax.set_xlabel('Score Fields')
ax.set_ylabel('Accuracy (%)')

title_text = f"Model: {model}, Prompt: {prompt}, Score Distributions Across Problems"
ax.set_title(title_text)

# Set x-axis tick labels to score field names
plt.xticks(np.arange(len(score_fields)), score_fields, rotation=45, ha='right')

# Add legend and grid
ax.legend(title='Legend', bbox_to_anchor=(1, 1), ncol=1)

ax.grid(True)

# Show the plot
plt.tight_layout()
plt.savefig(os.path.join(target_out_dir, f'{model}_{prompt}_scores_plot.png'))
plt.savefig(os.path.join(target_out_dupe_dir, f'{model}_{prompt}_scores_plot.png'))

plt.show()
