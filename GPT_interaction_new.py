### this one is without prev. reference 

import os
from openai import AzureOpenAI
import openai
import json

# Define a chat function using API
def chat(prompt, model):
    # Ensure the API key is retrieved from the environment variable
    AZURE_OPENAI_API_KEY = "037155e1b16a432fa836637370eca0e3"
    api_key = "037155e1b16a432fa836637370eca0e3"
    if api_key is None:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is not set")
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key=api_key,
        api_version="2024-02-15-preview"
    )
    
    message_text = [{"role": "system", "content": ""}, {"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=model,  # model = "deployment_name"
        messages=message_text,
        temperature=0,
        max_tokens=200,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return completion

# Data loader function
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_problems_and_solutions(problems_dir, solutions_dir):
    problem_solution_pairs = []

    for filename in os.listdir(problems_dir):
        if filename.endswith('.json'):
            problem_file_path = os.path.join(problems_dir, filename)
            solution_file_path = os.path.join(solutions_dir, filename)
            
            problem_data = load_json_from_file(problem_file_path)
            solution_data = load_json_from_file(solution_file_path)
            
            source_language = problem_data.get("source_language")
            target_language = problem_data.get("target_language")
            test_problems = problem_data.get("test", [])
            test_solutions = solution_data.get("test", [])

            min_len = min(len(test_problems), len(test_solutions))
            for i in range(min_len):
                problem_solution_pairs.append({
                    "source_language": source_language,
                    "target_language": target_language,
                    "problem": test_problems[i],
                    "solution": test_solutions[i]
                })

    return problem_solution_pairs

# Interactive GPT function
def iterative_gpt_interaction(initial_prompt, actual_problems, actual_solution, gpt4_iterations, gpt35_iterations):
    current_prompt = initial_prompt

    initial_prompt_for_gpt4 = f"Here we are providing the solution for each problem, so that you can use these hint to generate an optimized solution from gpt35turbo, so please use the solution part and Generate hints for the following problem:\n{actual_problems}\n\nSolution: {actual_solution}\n\nHints:"
    hints = chat(initial_prompt_for_gpt4, "gpt4")
    hints_content = hints.choices[0].message.content

    response_content=None

    for i in range(gpt4_iterations):
        response = chat(f"{current_prompt}\n\nHints:\n{hints_content}", "gpt35turbo")
        response_content = response.choices[0].message.content

        difference_analysis_prompt = f"Actual Solution: {actual_solution}\nGenerated Solution: {response_content}\n\nGenerate hints for the differences and how to improve the solution:"
        hints = chat(difference_analysis_prompt, "gpt4")
        hints_content = hints.choices[0].message.content

        current_prompt = response_content

    final_response = response_content.strip().split("\n")[0] 

    # print("problem:", actual_problems)
    # print("$$$$")
    # print("final response:",final_response)
    # print("%^^&^R")
    # if isinstance(response_content, str):
    #     # If response_content is a single string formatted as a list
    #     if response_content.startswith("[") and response_content.endswith("]"):
    #         # Convert string representation of list to actual list
    #         response_content_list = eval(response_content)
    #         final_response = next((text.strip() for text in response_content_list if text.strip() and text.strip() not in actual_problems and text.strip() not in ['>', '<']), "")
    #     else:
    #         # Directly process the string
    #         final_response = response_content.strip()
    # elif isinstance(response_content, list):
    #     # If response_content is a list, extract the relevant part
    #     final_response = next((text.strip() for text in response_content if text.strip() and text.strip() not in actual_problems and text.strip() not in ['>', '<']), "")
    # else:
    #     final_response = ""

    return final_response


# Prompt generation function
def make_prompt_intgpt(problem, solution):
    prompt = (f"Please carefully read the following problem and generate a concise solution using hints from GPT-4. "
              f"The solution should be in a single sentence, containing only the necessary words and symbols. "
              f"Do not include any extra symbols or words in the final response. "
              f"The response should be formatted as a single sentence surrounded by {{''}} and should not repeat the problem statement.\n\n"
              f"Problem:\n{problem}\n\n"
              )
    return prompt

def main():
    problems_dir = "datasets/PuzzLing/data_public_data_dev"  # Update with the correct path
    solutions_dir = "datasets/PuzzLing/data_public_reference_data_dev"  # Update with the correct path  
    output_dir = "output_directory_of_gpt_interactions"  # Update with the desired output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    problem_solution_pairs = load_problems_and_solutions(problems_dir, solutions_dir)

    results = {}
    
    for pair in problem_solution_pairs:
        source_language = pair["source_language"]
        target_language = pair["target_language"]
        problem = pair["problem"]
        solution = pair["solution"]
        
        final_response = None  # Initialize final_response to ensure it's defined

        #if source_language == "norwegian" and target_language == "english":
        initial_prompt = make_prompt_intgpt(problem,solution)
        final_response = iterative_gpt_interaction(initial_prompt, problem, solution, gpt4_iterations=1, gpt35_iterations=1)


        # initial_prompt = make_prompt_intgpt(problem)
        #     #try:
        # final_response = iterative_gpt_interaction(initial_prompt, problem, solution, gpt4_iterations=1, gpt35_iterations=1)
        #     # except Exception as e:
        #     #     print(f"Error processing problem: {problem}\nError: {e}")
        #     #     final_response = "Error processing this problem."
        
        if final_response:  # Only add to results if final_response is set
            language_pair = f"{source_language}-{target_language}"
            if language_pair not in results:
                results[language_pair] = []
            results[language_pair].append({
                "problem": problem,
                "solution": solution,
                "final_response": final_response
            })

    # Save results in language-specific files
    for language_pair, data in results.items():
        output_file_path = os.path.join(output_dir, f"{language_pair}.json")
        save_json_to_file(data, output_file_path)

if __name__ == "__main__":
    main()




###  this one is with prev. response 
    


# so this one is the updated code, in this we are using previous response while predicting the new problem 

import os
from openai import AzureOpenAI
import openai
import json

# Define a chat function using API
def chat(prompt, model):
    # Ensure the API key is retrieved from the environment variable
    AZURE_OPENAI_API_KEY = "037155e1b16a432fa836637370eca0e3"
    api_key = "037155e1b16a432fa836637370eca0e3"
    if api_key is None:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is not set")
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key=api_key,
        api_version="2024-02-15-preview"
    )
    
    message_text = [{"role": "system", "content": ""}, {"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=model,  # model = "deployment_name"
        messages=message_text,
        temperature=0,
        max_tokens=200,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return completion

# Data loader function
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_problems_and_solutions(problems_dir, solutions_dir):
    problem_solution_pairs = []

    for filename in os.listdir(problems_dir):
        if filename.endswith('.json'):
            problem_file_path = os.path.join(problems_dir, filename)
            solution_file_path = os.path.join(solutions_dir, filename)
            
            problem_data = load_json_from_file(problem_file_path)
            solution_data = load_json_from_file(solution_file_path)
            
            source_language = problem_data.get("source_language")
            target_language = problem_data.get("target_language")
            test_problems = problem_data.get("test", [])
            test_solutions = solution_data.get("test", [])

            min_len = min(len(test_problems), len(test_solutions))
            for i in range(min_len):
                problem_solution_pairs.append({
                    "source_language": source_language,
                    "target_language": target_language,
                    "problem": test_problems[i],
                    "solution": test_solutions[i]
                })

    return problem_solution_pairs

# Function to process conversation and get responses
# def process_prompts(prompts, client, model='gpt35turbo', max_tokens=300):
#     response_list = []
#     response_dict = {}
#     prev_response = ""  # To store the previous response

#     for i, prompt in enumerate(prompts):
#         message_text = [
#             {"role": "system", "content": prev_response},
#             {"role": "user", "content": prompt}
#         ]

#         completion = client.chat.completions.create(
#             model=model,  # Model name or deployment name
#             messages=message_text,
#             temperature=0,  # Reproducible results
#             max_tokens=max_tokens,
#             top_p=0.95,
#             frequency_penalty=0,
#             presence_penalty=0,
#             stop=None,
#         )
#         response_content = completion.to_dict()['choices'][0]['message']['content']
#         response_list.append(response_content)
#         response_dict[f'Prompt {i + 1}'] = response_content

#         prev_response = response_content  # Update the previous response

#         print(f"SUCCESS: Prompt {i + 1} processed.")

#     return response_dict, response_list

# Interactive GPT function
def iterative_gpt_interaction(initial_prompt, actual_problems, actual_solution, gpt4_iterations, gpt35_iterations, client):
    current_prompt = initial_prompt
    prev_response = ""  # To store the previous response

    initial_prompt_for_gpt4 = f"Here we are providing the solution for each problem, so that you can use these hints to generate an optimized solution from gpt35turbo. Please use the solution part as refereence  and generate hints for the following problem:\n{actual_problems}\n\nSolution: {actual_solution}\n\nHints:"
    hints = chat(initial_prompt_for_gpt4, "gpt4")
    hints_content = hints.choices[0].message.content

    response_content = None

    for i in range(gpt4_iterations):
        # Include the previous response in the system role
        message_text = [
            {"role": "system", "content": prev_response},
            {"role": "user", "content": f"{current_prompt}\n\nHints:\n{hints_content}"}
        ]
        response = client.chat.completions.create(
            model="gpt35turbo",
            messages=message_text,
            temperature=0,
            max_tokens=200,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        response_content = response.choices[0].message.content

        difference_analysis_prompt = f"Actual Solution: {actual_solution}\nGenerated Solution: {response_content}\n\nGenerate hints for the differences and how to improve the solution:"
        hints = chat(difference_analysis_prompt, "gpt4")
        hints_content = hints.choices[0].message.content

        prev_response = response_content  # Update the previous response
        current_prompt = response_content

    final_response = response_content

    # print("problem:", actual_problems)
    # print("$$$$")
    # print("final response:", final_response)
    # print("%^^&^")

    return final_response

# Prompt generation function
# def make_prompt_intgpt(problem, solution):
#     prompt = f"This is the problem \n\n{problem}, Please carefully read the problem first and generate the solution for the  problem using hint from gpt4 and the generated solution will not be in descriptive way it should be in the single sentence. and it should contain only required words and symbole and also please dont include any extra symbnol and words in the final response, and response would be the single sentence sorrounded by this  {{''}} only and also please dont use problem statement in our final response  ."
#     return prompt

def make_prompt_intgpt(problem, solution):
    prompt = (f"Please carefully read the following problem and generate a concise solution using hints from GPT-4. "
              f"The solution should be in a single sentence, containing only the necessary words and symbols. "
              f"Do not include any extra symbols or words in the final response. "
              f"The response should be formatted as a single sentence surrounded by {{''}} and should not repeat the problem statement.\n\n"
              f"Problem:\n{problem}\n\n"
              )
    return prompt


def main():
    problems_dir = "datasets/PuzzLing/data_public_data_dev"  # Update with the correct path
    solutions_dir = "datasets/PuzzLing/data_public_reference_data_dev"  # Update with the correct path  
    output_dir = "output_directory_of_gpt_interactions"  # Update with the desired output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    problem_solution_pairs = load_problems_and_solutions(problems_dir, solutions_dir)

    # Initialize the OpenAI client
    api_key = "037155e1b16a432fa836637370eca0e3"  # Replace with your actual API key
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key=api_key,
        api_version="2024-02-15-preview"
    )

    results = {}

    for pair in problem_solution_pairs:
        source_language = pair["source_language"]
        target_language = pair["target_language"]
        problem = pair["problem"]
        solution = pair["solution"]

        final_response = None  # Initialize final_response to ensure it's defined

        #if source_language == "..." and target_language == "english":
        initial_prompt = make_prompt_intgpt(problem, solution)
        final_response = iterative_gpt_interaction(initial_prompt, problem, solution, gpt4_iterations=1, gpt35_iterations=1, client=client)

        if final_response:  # Only add to results if final_response is set
            language_pair = f"{source_language}-{target_language}"
            if language_pair not in results:
                results[language_pair] = []
            results[language_pair].append({
                "problem": problem,
                "solution": solution,
                "final_response": final_response
            })

    # Save results in language-specific files
    for language_pair, data in results.items():
        output_file_path = os.path.join(output_dir, f"{language_pair}.json")
        save_json_to_file(data, output_file_path)

if __name__ == "__main__":
    main()



