# Teacher and Student Interactions Util code and workflow

import os
from openai import AzureOpenAI
import datetime
import json
import util_python_formatter as pyform
import util_multi_agent as agents


# Read examples from json file (produced golden)
def get_teacher_examples(examples_list, answers_list):
    examples = ''
    for i in range(len(examples_list)):
        examples += f'Original Sentence: {examples_list[i]}\nEngrypted Sentence: {answers_list[i]}\n\n'
    return examples


def get_teacher_skeleton_code():
    return f'''
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(example):

    # TODO: using the nltk module, construct the "new_sentence" that can encrypt each sentence from "examples".
    
    return new_sentence

# Examples
examples = [
    "The cat sat on the mat.",
    "Knowledge speaks louder than words.",
    "A shiny and brown fox jumps over the lazy rainbow.",
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))
    
# Save the list to JSON
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)

print(answers)
'''

def form_teacher_question(teacher_examples, teacher_skeleton_code):
    return f'''This is a word puzzle, where there are two secret rules that encrypt the sentence. Can you guess those rules, then use Python script to simulate this?

here are some examples: 

{teacher_examples}

First, carefully observe differences between the "original sentence" and "encrpted sentence".
Then, think about how a python code implementation can simulate this.
Then, please complet the "TODO" portion of the following python skeleton code, in the "encrypt_sentence()" function. 
Do not change anything else in the code. Also don't use any additional python modules.

```python
{teacher_skeleton_code}
```

Only return the Python code itself. No other explanations needed.
'''

def get_teacher_evaluation(teacher_examples, teacher_answers, student_answers):
    return f'''Now, can you compare against the teacher's output and the students' outputs?

    Again, the orininal puzzle pairs look like this:
    {teacher_examples}

    The teacher's outputs look like this:

    {teacher_answers}

    And these are the student's answers:

    {student_answers}

Looping through each elements of the two lists, think about how the "student" can correct the code, so that the outputs can match with that of the teacher. 
Can you give a one- or two-sentence hint with natural language, instead of python code?
Point out the differences between the expected output and the actual output, then make suggestions.
Only give the hints, nothing else.
'''


def get_student_hint(teacher_hint, teacher_answers, student_answers, teacher_skeleton_code):
    return f'''This is a good attempt. However, it's not exactly correct. Please consider the following hint:
    {teacher_hint}

Can you try again with the code implementation? Again, this is the answer key:

{teacher_answers}

And this is your previous response:

{student_answers}

Carefully observe the differences between the two outputs, and think about how you can correct the code.
Then, fill in this template, the same one as before:

```python
{teacher_skeleton_code}
```

'''

def revised_teacher_evaluation(teacher_answers, student_answers):
    return f'''The student has revised thier answer. Can you verify again?
   
    The original example:

    {teacher_answers}

    The student's answers:

    {student_answers}

If the answers look correct, please answer "test passed". Otherwise, answer "try again".
'''

def ask_for_student_comments():
    return f'''Your code works great! Can you explain your reasoning behind this code?
    Please answer in a few sentences, listing each step.
    Then, come up with a few new example pairs of the "original sentence" and "encrypted sentence" to test your code.'''


def main():
    # Help run the student code
    helper = pyform.ScriptHelper()
    file_name = 'student_script.py'

    # Set up GPT clients
    model_name = 'gpt4'
    teacher_convo = agents.Conversation(agents.load_model(model_name), model_name, 'Teacher')
    student_convo = agents.Conversation(agents.load_model(model_name), model_name, 'Student')
    
    # ------------------------- Conversation starts here -------------------------
    # Teacher gives question
    with open('teacher_examples.json', 'r', encoding='utf-8') as file:
        golden_questions = json.load(file)
    with open('teacher_answers.json', 'r', encoding='utf-8') as file:
        golden_answers = json.load(file)

    teacher_examples = get_teacher_examples(golden_questions, golden_answers)

    question = form_teacher_question(teacher_examples, get_teacher_skeleton_code())
    
    print(" --------------------------- TEACHER EXAMPLES --------------------------- ")
    print(question)
    print(" ------------------------------------------------------------- ")
    

    # Let the student explain its reasoning
    iter = 1
    
    # Helper runs student responses as a python script
    file_name = 'student_script01.py'
    helper.save_to_file(student_convo.process(question, 450), file_name)
    stdout, stderr = helper.run_script(file_name)

    print(f" --------------------------- STUDENT STDOUT {iter}--------------------------- ")
    print(f"Golden: {golden_answers}\nStudent: {stdout}")
    print(" ------------------------------------------------------------- ")
    iter += 1   
    
    # Use the json file to load student answers
    with open('student_answers.json', 'r', encoding='utf-8') as file:
        student_answers = json.load(file)

    # Compare student stdout with teacher evaluation
    prompt = get_teacher_evaluation(teacher_examples, golden_answers, student_answers)
    hint = teacher_convo.process(prompt, max_tokens=450)
    print(" --------------------------- HINT FIRST --------------------------- ")
    print(hint)
    print(" ------------------------------------------------------------- ")

    # Gives hint back to the student, then runs the student's code again
    student_hint = get_student_hint(hint, golden_answers, stdout, get_teacher_skeleton_code())
 
    file_name = 'student_script02.py'
    helper.save_to_file(student_convo.process(student_hint, 450), file_name)
    stdout, stderr = helper.run_script(file_name)
    
    print(f" --------------------------- STUDENT STDOUT {iter}--------------------------- ")
    print(f"Golden: {golden_answers}\nStudent: {stdout}")
    print(" ------------------------------------------------------------- ")
    iter += 1   


    # Teacher evaluates again
    prompt = revised_teacher_evaluation(golden_answers, stdout)

    print(" --------------------------- TEACHER EVAL --------------------------- ")
    print(prompt)
    print(" ------------------------------------------------------------- ")


    pass_fail_tag = teacher_convo.process(prompt, max_tokens=400)

    print(prompt)
    print(" --------------------------- PASS/FAIL --------------------------- ")
    print(pass_fail_tag)
    print(" ------------------------------------------------------------- ")

    
    if pass_fail_tag == "test passed":
        prompt = ask_for_student_comments()
        stdout = student_convo.process(prompt, max_tokens=400)
        print(" --------------------------- COMMENT --------------------------- ")
        print(stdout)
        print(" ------------------------------------------------------------- ")
    else:
        print("Student needs to try again.")
        # TODO: Add a loop to keep trying until the student passes the test
        while pass_fail_tag != "test passed" and iter < 5:
            # Compare student stdout with teacher evaluation
            prompt = get_teacher_evaluation(teacher_examples, golden_answers, stdout)
            hint = teacher_convo.process(prompt, 450)
            print(f" --------------------------- NEW HINT {iter}--------------------------- ")
            print(hint)
            print(" ------------------------------------------------------------- ")

            # Gives hint back to the student, then runs the student's code
            student_hint = get_student_hint(hint, golden_answers, stdout, get_teacher_skeleton_code())
         
            file_name = f'student_script0{iter}.py'
            helper.save_to_file(student_convo.process(student_hint, 450), file_name)
            stdout, stderr = helper.run_script(file_name)

            print(f" --------------------------- STUDENT STDOUT {iter}--------------------------- ")
            print(f"Golden: {golden_answers}\nStudent: {stdout}")
            print(" ------------------------------------------------------------- ")

            # Teacher evaluates again
            prompt = revised_teacher_evaluation(golden_answers, stdout)
            pass_fail_tag = teacher_convo.process(prompt, max_tokens=400)
            print(f" --------------------------- PASS/FAIL {iter} --------------------------- ")
            print(pass_fail_tag)
            print(" ------------------------------------------------------------- ")

            iter += 1


    print('ALL INTERACTIONS FINISHED.')

if __name__ == "__main__":
    main()
