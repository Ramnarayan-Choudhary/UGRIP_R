'''
util.py

UGRIP Linguistics Olympiad Project
Updated 06/08/2024 @12:40 PM by Huanying (Joy) Yeh

Content:
- Various utility functions for LLM response evaluation
'''

import os
import shutil
import json
import re
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import openpyxl
import os
import pickle
import datetime
# from xlsxwriter import Workbook


# Bool to check if the evaluation report already exists
def all_eval_report_exist(dir, list_of_models, list_of_prompts):
    for model in list_of_models:
        for prompt in list_of_prompts:
            if not os.path.exists(f'{dir}/{model}_{prompt}_scores_summary.csv'):
                return False    
    return True

# Bool to check if the evaluation report already exists
def this_eval_report_exists(dir, model, prompt):
    return os.path.exists(f'{dir}/{model}_{prompt}_scores_summary.csv')

def adjust_col_width(filename):
    wb = openpyxl.load_workbook(filename = filename)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        
        for col in ws.columns:
              max_length = 0
              column = col[0].column_letter # Get the column name
              for cell in col:
                  try: # Necessary to avoid error on empty cells
                      if len(str(cell.value)) > max_length:
                          max_length = len(str(cell.value))
                  except:
                      pass
              adjusted_width = (max_length + 2) * 1.1
              ws.column_dimensions[column].width = adjusted_width
              
              # Content center alignment
              for cell in col:
                  cell.alignment = openpyxl.styles.Alignment(horizontal='center', vertical='center')
    
    # new_file = out_filename
    wb.save(filename)
    wb.close()


def setup_test_bench(source_dir, target_dir, bool_edit_json_name):
    status_msgs = []
    try:
        for filename in os.listdir(source_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(source_dir, filename)
                
                # Extract the first 4 characters of the filename
                prefix = filename[:4]

                try:
                    # Load the JSON file
                    if bool_edit_json_name:
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                        source_language = data.get('source_language', '')
                        source_language = source_language.strip().replace(' ', '_')
                        source_language = re.sub(r'[^a-z]', '0', source_language)

                        new_filename = f"{prefix}_{source_language}_answers.json"
                        new_file_path = os.path.join(target_dir, 'res', new_filename)
                        shutil.copyfile(file_path, new_file_path)
                        # status_msgs.append(f"File '{filename}' copied and renamed as '{new_filename}' in the target directory.")
                    else:
                        shutil.copyfile(file_path, os.path.join(target_dir, 'res', filename))
                        # status_msgs.append(f"File '{filename}' copied in the target directory.")

                except (json.JSONDecodeError, KeyError) as e:
                    status_msgs.append(f"ERROR: Failed to process JSON file '{filename}': {e}")
                except IOError as e:
                    status_msgs.append(f"ERROR: Failed to copy file '{filename}': {e}")
                except Exception as e:
                    status_msgs.append(f"ERROR: Unexpected error processing file '{filename}': {e}")
        
        status_msgs.append(f"SUCCESS: LLM TEST BENCH SETUP ALL DONE for {source_dir}")
    except Exception as e:
        status_msgs.append(f"ERROR: Failed to list directory '{source_dir}': {e}")
    
    return "\n".join(status_msgs)


def create_eval_csv(output_dir_temp, output_dir_actual, model, prompt):
    status_msg = ""
    try:
        # Init regex patterns
        data_frames = []
        score_pattern = re.compile(r'(\w+_SCORE):\s*(\d+\.\d+)')

        # Loop through each file in the directory
        for filename in os.listdir(output_dir_temp):
            if filename.endswith("_scores.txt"):
                file_path = os.path.join(output_dir_temp, filename)
                with open(file_path, 'r') as file:
                    content = file.read()

                # Extract the scores from the content
                scores = score_pattern.findall(content)
                score_dict = {score[0]: float(score[1]) for score in scores}

                # Extract tag and target language from filename
                tag, target_lang = filename.split('_')[:2]

                # Add tag and target language to the dictionary
                if filename.endswith("overall_scores.txt"):
                    score_dict['tag'] = 'overall'
                    score_dict['target_lang'] = 'average'
                else:
                    score_dict['tag'] = tag
                    score_dict['target_lang'] = target_lang

                # Convert the dictionary to a DataFrame and append it to the list
                data_frames.append(pd.DataFrame([score_dict]))

        # Generate the dataframe
        df = pd.concat(data_frames, ignore_index=True)
        columns_order = ['tag', 'target_lang'] + [col for col in df.columns if col not in ['tag', 'target_lang']]
        df = df[columns_order]

        # 5. Delete the raw .txt files
        try:
            shutil.rmtree(output_dir_temp)
        except Exception as e:
            print(f"Error: {e}")

        # Save the DataFrame to a CSV file
        csv_filename = f'{model}_{prompt}_scores_summary.csv'
        csv_filepath = os.path.join(output_dir_actual, csv_filename)
        df.to_csv(csv_filepath, index=False)

        status_msg = f"SUCCESS: CSV file '{csv_filename}' saved to '{output_dir_actual}'."
        
    except FileNotFoundError as e:
        status_msg = f"ERROR: File not found. {e}"
    except pd.errors.EmptyDataError as e:
        status_msg = f"ERROR: No data found to concatenate. {e}"
    except Exception as e:
        status_msg = f"ERROR: An unexpected error occurred. {e}"

    return status_msg, df


def create_scores_plot_indiv(df, fig_out_dir, model, prompt):
    score_fields = np.array([col for col in df.columns if col not in ['tag', 'target_lang']])

    # Define the y-axis (accuracy, assuming scores are percentages)
    accuracy = df[score_fields]
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot scatter points for each problem (each row in the DataFrame)
    for i in range(len(df)):
        x = np.arange(len(score_fields))  # Generate x values as indices for score fields
        y = accuracy.iloc[i].values  # Select accuracy values for the current row
        
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

    out_filename = f'{model}_{prompt}_scores_plot.png'
    

    try: 
        plt.savefig(os.path.join(fig_out_dir, out_filename))
        status = f"SUCCESS: plotted {out_filename}."
        return status
    
    except Exception as e:
        print(f"Error: {e}")



def create_scores_plot_all(df, fig_out_dir):
    score_fields = np.array([col for col in df.columns if col not in ['model', 'prompt']])

    # Define the y-axis (accuracy, assuming scores are percentages)
    accuracy = df[score_fields]
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot scatter points for each problem (each row in the DataFrame)
    for i in range(len(df)):
        x = np.arange(len(score_fields))  # Generate x values as indices for score fields
        y = accuracy.iloc[i].values  # Select accuracy values for the current row
        
        ax.plot(x, y, label=f"{df['model'][i]}_{df['prompt'][i]}", linewidth=2.5)

    # Set labels and title
    ax.set_ylim([0, 110])
    ax.set_xlabel('Score Fields')
    ax.set_ylabel('Accuracy (%)')

    title_text = f"All Models Score Distributions Across Problems"
    ax.set_title(title_text)

    # Set x-axis tick labels to score field names
    plt.xticks(np.arange(len(score_fields)), score_fields, rotation=45, ha='right')

    # Add legend and grid
    ax.legend(title='Legend', bbox_to_anchor=(1, 1), ncol=1)
    ax.grid(True)

    # Show the plot
    plt.tight_layout()

    out_filename = f'all_models_scores_plot.png'
    
    try: 
        plt.savefig(os.path.join(fig_out_dir, out_filename))
        status = f"SUCCESS: plotted {out_filename}."
        return status
    
    except Exception as e:
        print(f"Error: {e}")


# Initialize an empty DataFrame with specified column names
def create_all_models_eval_csv(output_dir_actual, list_of_models, list_of_prompts, out_csv_name):
    status_msg = ""
    column_names = ['Model', 'Prompt', 'EF_BLEU_SCORE','EF_CHRF_SCORE','EF_CTER_SCORE',
                    'EF_EM_SCORE','FE_BLEU_SCORE','FE_CHRF_SCORE','FE_CTER_SCORE',
                    'FE_EM_SCORE','BLEU_SCORE','CHRF_SCORE','CTER_SCORE','EM_SCORE']

    df = pd.DataFrame(columns=column_names)

    # Iterate over each file in the directory
    for model in list_of_models:
        for prompt in list_of_prompts:
            filename = f"{model}_{prompt}_scores_summary.csv"
            target_dir = os.path.join(output_dir_actual, filename)
            try:
                temp_df = pd.read_csv(target_dir)
                last_row_df = temp_df.iloc[-1, 2:].to_frame().T

                last_row_df.insert(0, 'model', model)
                last_row_df.insert(1, 'prompt', prompt)
                df = pd.concat([df, last_row_df], ignore_index=True)
            
            except pd.errors.EmptyDataError:
                status_msg = f"ERROR: The file '{filename}' is empty."
            except Exception as e:
                status_msg = f"ERROR: An error occurred while processing the file '{filename}'. {e}"

            # Set the column names to the specified ones (only if they match in length)
            if len(df.columns) == len(column_names):
                df.columns = column_names
            else:
                status_msg = "ERROR: The number of specified column names does not match the number of columns in the data."
        
        # 4. save the DataFrame to a CSV file
        out_csv_path = os.path.join(output_dir_actual, out_csv_name)
        df.to_csv(out_csv_path, index=False)

        status_msg = f"SUCCES: {out_csv_name} is saved."
    return status_msg, df


