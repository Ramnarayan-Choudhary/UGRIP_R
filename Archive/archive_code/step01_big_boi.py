# Re-name very long sentences
# Save the file to the correct location
import os
import shutil
import json
import re
import data_evaluation_script.evaluate as evaluate

from data_evaluation_script.eval_submission_file import evaluate_file
from data_evaluation_script.util import add_dict_to_dict, combine_dicts


# -------------- STEP 1: COPY AND RENAME JSON FILES -----------------
# This doesn't change at all (for eval function call)
target_directory = 'AAA_My_PuzzLing_Test_Bench/res'
os.makedirs(target_directory, exist_ok=True)

# This loops through
list_of_models = ['GPT_35_TURBO', 'GPT_4', 'LLAMA-3', 'MISTRAL']
list_of_prompts = ['BASIC', 'LONGER', 'COT']

# for model in list_of_models:
#     for prompt in list_of_prompts:

model = 'GPT_4'
prompt = 'BASIC'
# prompt = 'COT'

source_directory = f'{model}/{prompt}'

# Loop through each file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(source_directory, filename)
        
        # Extract the first 4 characters of the filename
        prefix = filename[:4]
        
        # Load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        source_language = data.get('source_language', '')
        source_language = source_language.strip().replace(' ', '_')
        source_language = re.sub(r'[^a-z]', '0', source_language)
        new_filename = f"{prefix}_{source_language}_answers.json"
        new_file_path = os.path.join(target_directory, new_filename)
        
        shutil.copyfile(file_path, new_file_path)
        print(f"File '{filename}' copied and renamed as '{new_filename}' in the target directory.")


target_out_dir = f'{model}_{prompt}_EVAL'

## -------------- STEP 2: EVALUATE THE FILES -----------------
import subprocess

# Define the command to call
# command = 'python3 C:\Users\joy20\Folder\SU_2024\UGRIP\data_evaluation_script\evaluate.py C:\Users\joy20\Folder\SU_2024\UGRIP\AAA_My_PuzzLing_Test_Bench C:\Users\joy20\Folder\SU_2024\UGRIP\AAA_SCORES'

command = 'python3 C:\\Users\\joy20\\Folder\\SU_2024\\UGRIP\\data_evaluation_script\\evaluate.py C:\\Users\\joy20\\Folder\\SU_2024\\UGRIP\\AAA_My_PuzzLing_Test_Bench C:\\Users\\joy20\\Folder\\SU_2024\\UGRIP\\AAA_SCORES'

# Execute the command
subprocess.run(command)