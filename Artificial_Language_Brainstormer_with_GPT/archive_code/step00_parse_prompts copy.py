import os
import openai
import datetime

# Function to load the specified LLM model
def load_model():
    print("Loading the model...")
    client = openai
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    print("Model loaded successfully.")
    return client

# Function to read conversation data from a .txt file
def read_conversation_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    prompts = []
    current_prompt = ""
    is_prompt = False

    for line in lines:
        if line.startswith(">>>> Prompt"):
            is_prompt = True
            if current_prompt:
                prompts.append(current_prompt.strip())
            current_prompt = ""  # Reset current_prompt without adding the ">>>> Prompt" line
        elif line.startswith(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"):
            is_prompt = False
            if current_prompt:
                prompts.append(current_prompt.strip())
            current_prompt = ""
        elif line.startswith("--------") or line.startswith(">>>>---------"):
            is_prompt = False
            current_prompt = ""
        elif is_prompt:
            current_prompt += line

    if current_prompt:
        prompts.append(current_prompt.strip())
    
    return prompts

# Function to process conversation and get responses
def process_prompts(prompts, client):
    response_dict = {}
    for prompt in prompts:
        prompt_lines = prompt.split("\n")
        prompt_title = prompt_lines[0]
        prompt_content = "\n".join(prompt_lines[1:])
        prompt_key = f"Prompt {len(response_dict) + 1}"

        print(f"Sending {prompt_key}")
        response = client.Completion.create(
            model='gpt-3.5-turbo',
            prompt=prompt_content,
            temperature=0.8,
            max_tokens=1024,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["-----------------------------------------"],
        )
        response_content = response['choices'][0]['text'].strip()
        response_dict[prompt_key] = response_content
        print(f"Received response: {response_content}")
    
    return response_dict


# Main function to run the script
def main():
    input_file = 'input.txt'  # Replace with your input file path
    client = load_model()
    prompts = read_conversation_from_file(input_file)
    # responses = process_prompts(prompts, client)


    print(prompts[0])
    # output_lines = insert_responses_to_lines(lines, responses)

    # # Save to the output file
    # output_file = 'GPT_responses01.txt'
    # with open(output_file, 'w') as file:
    #     file.writelines(output_lines)
    #     print(f"Responses saved to {output_file}")

    # print("All tasks completed successfully.")

if __name__ == "__main__":
    main()
