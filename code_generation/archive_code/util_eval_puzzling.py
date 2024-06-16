'''
util.py

UGRIP Linguistics Olympiad Project
Updated 06/10/2024 @11:30 AM by Huanying (Joy) Yeh

Content:
- Various utility functions for LLM response evaluation
- Main function: llm_evaluate.py
'''

import os
import shutil
import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Checks if all evaluation report already exists
def all_eval_report_exist(dir, list_of_source_langs, list_of_target_langs):
    for source_lang in list_of_source_langs:
        for target_lang in list_of_target_langs:
            if not os.path.exists(f'{dir}/{source_lang}_{target_lang}_scores_summary.csv'):
                return False    
    return True


# Checks if a single report already exists
def this_eval_report_exists(dir, source_lang, target_lang):
    return os.path.exists(f'{dir}/{source_lang}_{target_lang}_scores_summary.csv')


# Copies the JSON files from the source directory to the target directory
def setup_test_bench(source_dir, target_dir, bool_edit_json_name=False):
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
                        with open(file_path, 'r', encoding='utf-8') as file:
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



# Combines all the temporary .txt files into a single .csv file
# Save to f'{output_dir_actual}/all_scores_summary.csv'
def create_eval_csv_global(output_dir_temp, output_dir_actual):

    print(output_dir_actual)
    print(output_dir_temp)
    status_msg = ""
    try:
        # Init regex patterns
        data_frames = []
        score_pattern = re.compile(r'(\w+_SCORE):\s*(\d+\.\d+)')

        # Loop through each file in the directory
        for filename in os.listdir(output_dir_temp):
            if filename.endswith(f"_scores.txt"):

                file_path = os.path.join(output_dir_temp, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Extract the scores from the content
                scores = score_pattern.findall(content)
                score_dict = {score[0]: float(score[1]) for score in scores}

                # Extract source_lang and target language from filename       
                source_lang, target_lang = filename.split('_')[:2]
                score_dict['source_lang'] = source_lang
                score_dict['target_lang'] = target_lang

                # Convert the dictionary to a DataFrame and append it to the list
                data_frames.append(pd.DataFrame([score_dict]))

        # Generate the dataframe
        df = pd.concat(data_frames, ignore_index=True)
        columns_order = ['source_lang', 'target_lang'] + [col for col in df.columns if col not in ['source_lang', 'target_lang']]
        df = df[columns_order]

        # 5. Delete the raw .txt files
        # try:
        #     shutil.rmtree(output_dir_temp)
        # except Exception as e:
        #     print(f"Error: {e}")

        # Save the DataFrame to a CSV file
        csv_filename = f'GPT4_global_all_scores_summary.csv'
        csv_filepath = os.path.join(output_dir_actual, csv_filename)
        df.to_csv(csv_filepath, index=False, encoding='utf-8')

        status_msg = f"SUCCESS: CSV file '{csv_filename}' saved to '{output_dir_actual}'."
        
    except FileNotFoundError as e:
        status_msg = f"ERROR: File not found. {e}"
    except pd.errors.EmptyDataError as e:
        status_msg = f"ERROR: No data found to concatenate. {e}"
    except Exception as e:
        status_msg = f"ERROR: An unexpected error occurred. {e}"

    return status_msg, df


# Plot the per-problem score summary for a source_lang and target_lang
# out_filename = f'{source_lang}_{target_lang}_scores_plot.png'

def create_scores_plot_indiv(df, fig_out_dir, source_lang, target_lang, colors_of_problem):

    # Re-order languages based on difficulty
    # custom_order = list(colors_of_problem.keys())
    # df['target_lang'] = pd.Categorical(df['target_lang'], categories=custom_order, ordered=True)
    # df = df.sort_values(by='target_lang')
    # df = df.reset_index(drop=True)

   
  
    # Define the y-axis (accuracy, assuming scores are percentages)
    score_fields = np.array([col for col in df.columns if col not in ['source_lang', 'target_lang']])
    accuracy = df[score_fields]

    _, ax = plt.subplots(figsize=(10, 6))
    for i in range(len(df)):
        x = np.arange(len(score_fields))  # Generate x values as indices for score fields
        y = accuracy.iloc[i].values  # Select accuracy values for the current row
        source_lang = df['source_lang'][i]
        lang = df['target_lang'][i]
        ax.plot(x, y, label=f"{df['source_lang'][i]}_{lang}", linewidth=2.5, color=colors_of_problem[source_lang])

    # Set labels and title
    ax.set_ylim([0, 110])
    ax.set_xlabel('Score Fields')
    ax.set_ylabel('Accuracy (%)')

    title_text = f"source_lang: {source_lang}, target_lang: {target_lang}, Score Distributions Across Problems"
    ax.set_title(title_text)

    # Set x-axis tick labels to score field names
    plt.xticks(np.arange(len(score_fields)), score_fields, rotation=45, ha='right')

    # Add legend and grid
    ax.legend(title='Legend', bbox_to_anchor=(1, 1), ncol=1)
    ax.grid(True)

    # Show the plot
    plt.tight_layout()
    out_filename = f'{source_lang}_{target_lang}_scores_plot.png'
    
    try: 
        plt.savefig(os.path.join(fig_out_dir, out_filename))
        status = f"SUCCESS: created {out_filename}."
        return status
    
    except Exception as e:
        print(f"Error: {e}")


def create_scores_bars_indiv(df, fig_out_dir, source_lang, target_lang, colors_of_problem):
     
    # Select target languages and their respective scores (excluding 'overall')
    target_langs = df['target_lang'][:-1]
    EF_BLEU_SCORE = df['BLEU_SCORE'][:-1]
    CHRF_SCORE = df['CHRF_SCORE'][:-1]
    CTER_SCORE = df['CTER_SCORE'][:-1]
    EM_SCORE = df['EM_SCORE'][:-1]
     
    # Set the width of the bars
    bar_width = 0.2
     
    # Set the positions of the bars on the x-axis
    r1 = np.arange(len(target_langs))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
     
    # Create the bar plot
    plt.figure(figsize=(14, 7))
    plt.bar(r1, EF_BLEU_SCORE, color="#ffb76f", width=bar_width, edgecolor='grey', label='BLEU_SCORE')
    plt.bar(r2, EM_SCORE, color="#800080", width=bar_width, edgecolor='grey', label='EM_SCORE')
    plt.bar(r3, CHRF_SCORE, color="#5fdaea", alpha=0.3, width=bar_width, edgecolor='grey', label='CHRF_SCORE')
    plt.bar(r4, CTER_SCORE, color="#8bff8b", alpha=0.3, width=bar_width, edgecolor='grey', label='CTER_SCORE')
     
    # Add xticks on the middle of the group bars
    plt.xlabel('Target Language', fontweight='bold')
    plt.xticks([r + bar_width for r in range(len(target_langs))], target_langs, rotation=45)
     
    # Add labels and title
    plt.ylabel('Accuracy (%)', fontweight='bold')
    plt.title(f'{source_lang}_{target_lang} PuzzLing Scores')
     
    # Create legend & Show graphic
    plt.legend()
    plt.tight_layout()

    out_filename = f'{source_lang}_{target_lang}_bars.png'
    
    try: 
        plt.savefig(os.path.join(fig_out_dir, out_filename))
        status = f"SUCCESS: created {out_filename}."
        return status
    
    except Exception as e:
        print(f"Error: {e}")

# Plot the score summary for all source_langs and target_langs
# out_filename = f'all_source_langs_scores_plot.png'
def create_scores_plot_all(df, fig_out_dir, colors, out_filename):
    score_fields = np.array([col for col in df.columns if col not in ['source_lang', 'target_lang']])
    accuracy = df[score_fields]
  
    for k in range(4):
        _, ax = plt.subplots(figsize=(10, 6))
        for i in range(3 * k , 3 * k + 3):
            x = np.arange(len(score_fields))  # Generate x values as indices for score fields
            y = accuracy.iloc[i].values  # Select accuracy values for the current row
        
            ax.plot(x, y, label=f"{df['source_lang'][i]}_{df['target_lang'][i]}", linewidth=2.5, color=colors[i])

        # Set labels and title
        ax.set_ylim([0, 110])
        ax.set_xlabel('Score Fields')
        ax.set_ylabel('Accuracy (%)')

        source_lang = df['source_lang'][i]
        title_text = f'{source_lang}_various_global_language_responses.png'
        ax.set_title(title_text)

        # Set x-axis tick labels to score field names
        plt.xticks(np.arange(len(score_fields)), score_fields, rotation=45, ha='right')

        # Add legend and grid
        ax.legend(title='Legend', bbox_to_anchor=(1, 1), ncol=1)
        ax.grid(True)

        # Show the plot
        plt.tight_layout()

        out_filename = f"{source_lang}_3_global_question_responses.png"

        try: 
            plt.savefig(os.path.join(fig_out_dir, out_filename))

        except Exception as e:
            print(f"Error: {e}")
    status = f"SUCCESS: plotted {out_filename}."
    return status



def create_scores_bars_all(df, fig_out_dir):

    # Select target languages and their respective scores (excluding 'overall')
    target_source_langs = df['source_lang']
    target_target_langs = df['target_lang']
    EF_BLEU_SCORE = df['BLEU_SCORE']
    CHRF_SCORE = df['CHRF_SCORE']
    CTER_SCORE = df['CTER_SCORE']
    EM_SCORE = df['EM_SCORE']
     
    # Set the width of the bars
    bar_width = 0.2
     
    # Set the positions of the bars on the x-axis
    r1 = np.arange(len(target_source_langs))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
     
    # Create the bar plot
    plt.figure(figsize=(15, 7))
    plt.bar(r1, EF_BLEU_SCORE, color="#ffb76f", width=bar_width, edgecolor='grey', label='BLEU_SCORE')
    plt.bar(r2, EM_SCORE, color="#800080", width=bar_width, edgecolor='grey', label='EM_SCORE')
    plt.bar(r3, CHRF_SCORE, color="#5fdaea", alpha=0.3, width=bar_width, edgecolor='grey', label='CHRF_SCORE')
    plt.bar(r4, CTER_SCORE, color="#8bff8b", alpha=0.3, width=bar_width, edgecolor='grey', label='CTER_SCORE')
     
    # Add xticks on the middle of the group bars
    plt.xlabel('Target Language', fontweight='bold')
    plt.xticks([r + bar_width for r in range(len(target_source_langs))], 
               [f"{df['source_lang'][r]}_{df['target_lang'][r]}" for r in range(len(target_source_langs))], rotation=45)
     
    # Add labels and title
    plt.ylabel('Accuracy (%)', fontweight='bold')
    plt.title(f'All LLMs PuzzLing Scores')
     
    # Create legend & Show graphic
    plt.legend()
    plt.tight_layout()

    out_filename = f'all_LLMs_scores_bars.png'
    
    try: 
        plt.savefig(os.path.join(fig_out_dir, out_filename))
        status = f"SUCCESS: created {out_filename}."
        return status
    
    except Exception as e:
        print(f"Error: {e}")

# Create the all_source_langs_scores_summary.csv file
def create_all_source_langs_eval_csv(output_dir_actual, list_of_source_langs, list_of_target_langs, out_csv_name):
    status_msg = ""
    column_names = ['source_lang', 'target_lang', 'EF_BLEU_SCORE','EF_CHRF_SCORE','EF_CTER_SCORE',
                    'EF_EM_SCORE','FE_BLEU_SCORE','FE_CHRF_SCORE','FE_CTER_SCORE',
                    'FE_EM_SCORE','BLEU_SCORE','CHRF_SCORE','CTER_SCORE','EM_SCORE']

    df = pd.DataFrame(columns=column_names)

    # Iterate over each file in the directory
    for source_lang in list_of_source_langs:
        for target_lang in list_of_target_langs:
            filename = f"{source_lang}_{target_lang}_scores_summary.csv"
            target_dir = os.path.join(output_dir_actual, filename)
            try:
                temp_df = pd.read_csv(target_dir)
                last_row_df = temp_df.iloc[-1, 2:].to_frame().T

                last_row_df.insert(0, 'source_lang', source_lang)
                last_row_df.insert(1, 'target_lang', target_lang)
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

