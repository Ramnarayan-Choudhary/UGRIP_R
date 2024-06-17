# Teacher and Student Interactions Util code and workflow

import os
import datetime
import json
import util_multi_agent as agents

import re

# Read examples from json file (produced golden)
def get_teacher_examples(examples_list, answers_list):
    examples = ''
    for i in range(len(examples_list)):
        examples += f'Original Sentence: {examples_list[i]}\nEncrypted Sentence: {answers_list[i]}\n\n'
    return examples


def form_teacher_question(teacher_examples):
    return f'''This is a word puzzle, where there are two secret rules that encrypt the sentence. 
    Can you guess those rules, then use Python script to simulate this?
Here are some examples: 

{teacher_examples}First, carefully observe differences between the "original sentence" and "encrpted sentence".
Can you list a few ideas on how the sentences are encrypted?
Only give the list, no other content needed.

It's a language puzzle, so think about word tokenization, part of speech tagging, and sentence construction.
The sentences need to make grammatical sense and express complete meanings.'''

def get_teacher_evaluation_old(teacher_examples, teacher_answers, student_answers):
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
Only give the hints, nothing else.'''

def get_teacher_evaluation(teacher_examples, teacher_answers, student_answers):
    return f'''Now, can you compare against the teacher's output and the students' outputs?

    Again, the orininal puzzle pairs look like this:
    {teacher_examples}

    The teacher's outputs look like this:

    {teacher_answers}

    And these are the student's answers:

    {student_answers}

Looping through each elements of the two lists, think about how the "student" can correct the code, so that the outputs can match with that of the teacher. 
Point out the differences between the expected output and the actual output.
Don't analyze the pairings one by one, rather, give some common mistakes and list 2 - 3 hints.
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
    # Set up GPT clients and Python local helper
    import io
    import sys

    # Save the content to a file
    file_path = "madak_history.txt"

    # Create a StringIO object to capture the output
    output_buffer = io.StringIO()

    # Redirect standard output to the StringIO object
    sys.stdout = output_buffer

    # Reset standard output to its original value
    sys.stdout = sys.__stdout__

    model_name = 'gpt4'
    teacher_convo = agents.Conversation(agents.load_model(model_name), model_name, 'Teacher')
    student_convo = agents.Conversation(agents.load_model(model_name), model_name, 'Student')
    helper = agents.ScriptHelper()

    teacher_test_script_name = 'step01_teacher_test_run_01.py'

    # ------------------------- Conversation starts here -------------------------
    # Teacher gives question
    with open('teacher_examples.json', 'r', encoding='utf-8') as file:
        golden_questions = json.load(file)
    with open('teacher_answers.json', 'r', encoding='utf-8') as file:
        golden_answers = json.load(file)

    teacher_examples = get_teacher_examples(golden_questions, golden_answers)
    skeleton_code = f'''
    import json
    from nltk import pos_tag
    from nltk.tokenize import word_tokenize

    def to_camel_case(word):
        return word[0].upper() + word[1:] if word else word

    def encrypt_sentence(sentence):
        # Convert the entire sentence to lowercase
        sentence = sentence.lower()
        
        # Remove dot
        if sentence[-1] == '.':
            sentence = sentence[:-1]
            
        # TO DO: YOUR CODE
        
        # Convert the letter from sentence to CamelCase
        sentence[0].upper() + sentence[1:]
        
        # Join the words back into a sentence and add a period at the end
        new_sentence = ' '.join(words) + '.'
        
        return new_sentence

    # Examples
    examples = {teacher_examples}

    answers = []
    for example in examples:
        answers.append(encrypt_sentence(example))

    # Save the list to JSON
    with open("student_answers.json", "w", encoding='utf-8') as json_file:
        json.dump(answers, json_file)
    print(answers)'''.format(teacher_examples)
    exam_question = form_teacher_question(teacher_examples)

    print(" --------------------------- TEACHER EXAM QUESTION ----------- ")
    print(exam_question)
    print(" ------------------------------------------------------------- ")

    # Let the student explain its reasoning before coding
    student_guessed_patterns = student_convo.process(exam_question, 1024)
    print(" --------------------------- STUDENT GUESSED PATTERNS --------------------------- ")
    print(f"Student Guessed Pattenrns:\n{student_guessed_patterns}" )
    print(" ------------------------------------------------------------- ")


    guiding_question = f'''You just mentioned the following patterns:
    {student_guessed_patterns}. Now, can you implement this in Python code?

    Please fill in the TODO section in the following code snippet. Don't change anything else:
    {skeleton_code}

    Only return the code snippet, nothing else.
    '''
    iter = 1

    # Very first student attempt
    file_name = f'student_script0{iter}.py'
    helper.save_to_file(student_convo.process(guiding_question, 1024), file_name)
    stdout, _ = helper.run_script(file_name)
    print(f" --------------------------- STUDENT STDOUT {iter}--------------------------- ")
    print(f"Golden: {golden_answers}\nStudent: {stdout}")
    print(" ------------------------------------------------------------- ")  

    prompt = get_teacher_evaluation(teacher_examples, golden_answers, stdout)
    raw_hint = teacher_convo.process(prompt, max_tokens=1024)
    full_hint = get_student_hint(raw_hint, golden_answers, stdout, skeleton_code)
    print(f" --------------------------- HINT #{iter} --------------------------- ")
    print(raw_hint) # Only list hints
    print(" ------------------------------------------------------------- ")


    iter = 2
    # Very first student attempt
    file_name = f'student_script0{iter}.py'
    helper.save_to_file(student_convo.process(guiding_question, 1024), file_name)
    stdout, _ = helper.run_script(file_name)
    print(f" --------------------------- STUDENT STDOUT {iter}--------------------------- ")
    print(f"Golden: {golden_answers}\nStudent: {stdout}")
    print(" ------------------------------------------------------------- ")  


    # Very first teacher eval
    prompt = revised_teacher_evaluation(golden_answers, stdout)
    print(" --------------------------- TEACHER EVAL --------------------------- ")
    print(prompt)
    print(" ------------------------------------------------------------- ")
    pass_fail_tag = teacher_convo.process(prompt, max_tokens=1024).lower()
    print(" --------------------------- PASS/FAIL --------------------------- ")
    print(pass_fail_tag)
    print(" ------------------------------------------------------------- ")

    bool_passed = "passed" in pass_fail_tag.lower()

    while iter < 15:
        if bool_passed:
            prompt = ask_for_student_comments()
            stdout = student_convo.process(prompt, max_tokens=1024)
            print(f" -------------------------- TEST PASSED AT ITER #{iter}. STUDENT COMMENT: --------------------------- ")
            print(stdout)
            print(" ------------------------------------------------------------- ")
            
            with open('student_answers.json', 'r', encoding='utf-8') as file:
                student_answers = json.load(file)

            print(f"----- PASSED AT ITER #{iter}). The final outputs are: ------------")
            print(f"Golden: {golden_answers}\nStudent: {student_answers}")
            print(" ------------------------------------------------------------- ")
            print('ALL INTERACTIONS FINISHED.')
            break
        else: # The student attempt loop 
            # 1. Teacher gives hint
            prompt = get_teacher_evaluation(teacher_examples, golden_answers, stdout)
            raw_hint = teacher_convo.process(prompt, max_tokens=1024)
            full_hint = get_student_hint(raw_hint, golden_answers, stdout, skeleton_code)
            print(f" --------------------------- HINT #{iter} --------------------------- ")
            print(raw_hint)
            print(" ------------------------------------------------------------- ")
            
            # 2. Student attempt
            file_name = f'student_script0{iter}.py'
            helper.save_to_file(student_convo.process(full_hint, 1024), file_name)
            stdout, _ = helper.run_script(file_name)
            print(f" --------------------------- STUDENT STDOUT {iter}--------------------------- ")
            print(f"Golden: {golden_answers}\nStudent: {stdout}")
            print(" ------------------------------------------------------------- ")

            # 3. Teacher grades
            prompt = revised_teacher_evaluation(golden_answers, stdout)
            print(f" --------------------------- TEACHER EVAL #{iter} --------------------------- ")
            pass_fail_tag = teacher_convo.process(prompt, max_tokens=1024).lower()
            print(f" --------------------------- PASS/FAIL #{iter} --------------------------- ")
            print(pass_fail_tag)
            print(" ------------------------------------------------------------- ")
            bool_passed = "passed" in pass_fail_tag.lower()
            iter += 1

    with open('student_answers.json', 'r', encoding='utf-8') as file:
        student_answers = json.load(file)
    print(f"----- FAILED, reached max iterations #{iter}. The final outputs are: ------------")
    print(f"Golden: {golden_answers}\nStudent: {student_answers}")
    print(" ------------------------------------------------------------- ")
    print('ALL INTERACTIONS FINISHED.')

    # Get the content from the StringIO object
    output_content = output_buffer.getvalue()


    with open(file_path, "w") as file:
        file.write(output_content)

    print(f"The printed message has been saved to {file_path}.")

if __name__ == "__main__":
    main()
