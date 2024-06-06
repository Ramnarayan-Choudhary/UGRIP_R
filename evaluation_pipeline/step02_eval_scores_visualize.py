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

# 1. Specify target directory (using raw string to avoid unicode escape issues)
target_dir = r'C:\Users\joy20\Folder\SU_2024\UGRIP\My_PuzzLing_Test_Bench\scores'

# Init regex patterns
data_frames = []
score_pattern = re.compile(r'(\w+_SCORE):\s*(\d+\.\d+)')

# 2. Loop through each file in the directory
for filename in os.listdir(target_dir):
    if filename.endswith("_scores.txt"):
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
df.to_csv(os.path.join(target_dir, 'scores_summary.csv'), index=False)
