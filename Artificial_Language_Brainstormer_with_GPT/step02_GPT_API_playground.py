'''
UGRIP 2024 - Linguistic Olynpiad Project
Designing an Artificial Language with Chat-GPT API
step00_parse_prompts.py

Content:
- Input a well-formatted list of prompts from a .txt file
- Process the prompts using Chat-GPT API
- Save the responses to a .json file
- Generate a human-readable conversation history to a .txt file
- Include time stamps in the file names for easy tracking

TODO:
- Prevent excessively long chat histories (runtime takes a lont time)!
- Down-stream processing + "student" model needs to be implemented
- Play with more detailed prompting.
'''

import datetime
from util_gpt import *
# Main function to run the script

def main():

    # ------------- [INPUTS]----------------
    input_prefix = 'joy_prompt'
    bool_save_json = True
    max_tokens = 500
    # -------------------------------------

    # Config don't change
    input_file = f'input_prompts/{input_prefix}.txt'  

    # Talk to Chat-GPT
    client = load_model()
    prompts = read_convo_from_file(input_file)
    response_dict, responses = process_prompts(prompts, client, max_tokens)
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")

    save_convo_to_txt(input_file, input_prefix, responses, timestamp)

    if bool_save_json:
        save_convo_to_json(response_dict, input_prefix, timestamp)  

    print('\nAll tasks completed successfully.')

if __name__ == "__main__":
    main()
