# Teacher and student interactions
# Updated 06/16/2024

import openai 
import nltk

from openai import AzureOpenAI
import json
import nltk
import os
import datetime
import util_gpt as gpt
import util_prompt_creation as prompting
import time


# Download NLTK data (if not already installed)
nltk.download('punkt')

# Load the specified LLM model

print("Loading GPT4...")
client = AzureOpenAI(
    azure_endpoint="https://cullmsouthindia.openai.azure.com/",
    api_key="037155e1b16a432fa836637370eca0e3",
    api_version="2024-02-15-preview"
)
print("SUCCESS: model loaded.")

def teacher_generate_questions():
    questions = [
        "What is the past tense of 'run'?",
        "What is the past tense of 'eat'?",
        # ... add more questions
    ]
    answers = [
        "ran",
        "ate",
        # ... add more answers
    ]
    return questions, answers

def teacher_grade_responses(questions, answers, student_responses):
    grades = []
    hints = []
    for i, (q, a, r) in enumerate(zip(questions, answers, student_responses)):
        if r == a:
            grades.append(True)
        else:
            grades.append(False)
            hints.append(f"Question {i+1}: Think more carefully about '{q.split()[-1]}' and similar verbs.")
    return grades, hints

def teacher_generate_questions_api():
    prompt = "Generate 10 examples to teach students the past tense in English."
    questions_and_answers = gpt_api_call(prompt)
    questions, answers = json.loads(questions_and_answers)
    return questions, answers

def teacher_grade_responses_api(questions, answers, student_responses):
    prompt = f"Questions: {questions}\nAnswers: {answers}\nStudent Responses: {student_responses}\nGrade the responses and provide hints."
    grading_and_hints = gpt_api_call(prompt)
    grades, hints = json.loads(grading_and_hints)
    return grades, hints

def student_generate_code_api(questions):
    prompt = f"Generate Python code to answer these questions: {questions}"
    responses = gpt_api_call(prompt)
    return json.loads(responses)

def student_revise_code_api(hints, student_responses):
    prompt = f"Hints: {hints}\nRevise the following code: {student_responses}"
    revised_responses = gpt_api_call(prompt)
    return json.loads(revised_responses)

def gpt_api_call(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def run_interaction_loop_api(max_iterations=3):
    questions, answers = teacher_generate_questions_api()
    student_responses = student_generate_code_api(questions)
    
    for iter in range(max_iterations):
        grades, hints = teacher_grade_responses_api(questions, answers, student_responses)
        if all(grades):
            print("All questions are correct!")
            break
        
        print("Grades:", grades)
        print("Hints:", hints)
        
        student_responses = student_revise_code_api(hints, student_responses)
        print("Revised Responses:", student_responses)

        print(f"Iteration {iter+1} completed.")

if __name__ == "__main__":
    num_iters = 1
    run_interaction_loop_api(num_iters)



