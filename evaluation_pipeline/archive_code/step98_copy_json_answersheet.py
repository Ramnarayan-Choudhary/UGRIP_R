import os
import shutil
import json
import re

source_directory = 'PuzzLing_Raw_Dataset/data_public_data_dev'
# target_directory = 'LLM_manual_cleanuppppp/base_prompt_puzzling'
target_directory = 'LLM_manual_cleanuppppp/longer_prompt_puzzling'
# Ensure the target directory exists, create it if it doesn't
os.makedirs(target_directory, exist_ok=True)

# Loop through each file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(source_directory, filename)
        
        # Extract the first 4 characters of the filename
        prefix = filename[:4]
        
        # Load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract the source language from the JSON data
        source_language = data.get('source_language', '')
        
        # Strip trailing spaces and replace center spaces with underscores
        source_language = source_language.strip().replace(' ', '_')
        
        source_language = re.sub(r'[^a-z]', '0', source_language)

        # Create the new filename based on the extracted information
        new_filename = f"{prefix}_{source_language}_answers.json"
        new_file_path = os.path.join(target_directory, new_filename)
        
        # Copy the file to the target directory with the new filename
        shutil.copyfile(file_path, new_file_path)

        print(f"File '{filename}' copied and renamed as '{new_filename}' in the target directory.")
