import re

# Extract the "template code" string from any runnable teacher Python file
def create_template_code_string(file_path):
    # Read the content of the Python file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    print(content)

    replacement01 = '''def encrypt_sentence(sentence):

    # TODO: Construct the "new_sentence" that can encrypt each sentence from "examples".
    
    return new_sentence
'''

    replacement02 = '''with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)
'''

    # Match and replace
    pattern01 = re.compile(r'def encrypt_sentence\(sentence\).*?return new_sentence\n', re.DOTALL)
    new_content = re.sub(pattern01, replacement01, content)

    pattern02 = re.compile(r'with open\("teacher_examples\.json", "w", encoding=\'utf-8\'\) as json_file:.*?print\("SUCCESS: teacher json files created."\)', re.DOTALL)
    new_content = re.sub(pattern02, replacement02, new_content)

    return new_content


print(create_template_code_string('step01_teacher_test_run_01.py'))