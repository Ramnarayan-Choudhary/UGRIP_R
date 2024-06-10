# Re-name very long sentences
# Save the file to the correct location
import os
import shutil
import json
import re


# -------------- STEP 1: COPY AND RENAME JSON FILES -----------------
# This doesn't change at all (for eval function call)
target_directory = 'AAA_My_PuzzLing_Test_Bench/res'
os.makedirs(target_directory, exist_ok=True)

# This loops through
list_of_models = ['GPT_35_TURBO', 'GPT_4', 'LLAMA_3', 'LLAMA_70B','MISTRAL']
list_of_prompts = ['BASIC', 'LONGER', 'COT']

# for model in list_of_models:
#     for prompt in list_of_prompts:
# model = 'LLAMA_70B'
# prompt = 'LONGER'

model = 'LLAMA_70B'
prompt = 'BASIC'

source_directory = f'{model}_RAW_ANSWERS/{prompt}'

bool_edit_json_name = False

# Loop through each file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(source_directory, filename)
        
        # Extract the first 4 characters of the filename
        prefix = filename[:4]
        
        # Load the JSON file
        if bool_edit_json_name:
            with open(file_path, 'r') as file:
                data = json.load(file)
        
            source_language = data.get('source_language', '')
            source_language = source_language.strip().replace(' ', '_')
            source_language = re.sub(r'[^a-z]', '0', source_language)
            new_filename = f"{prefix}_{source_language}_answers.json"
            new_file_path = os.path.join(target_directory, new_filename)

            shutil.copyfile(file_path, new_file_path)
            print(f"File '{filename}' copied and renamed as '{new_filename}' in the target directory.")

        else:
            shutil.copyfile(file_path, os.path.join(target_directory, filename))
            print(f"File '{filename}' copied in the target directory.")

print(f"SUCCESS: ALL DONE for {source_directory}\n")