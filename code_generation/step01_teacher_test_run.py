''' ----------------- NOTES START HERE -------------------
UGRIP 2024 - Linguistic Olympiad Project
Updated 06/17/2024

Content: the "teacher" experimental script that generates problem sets and ground truths.

Outputs:
- "lecture_outputs/teacher_examples.json"
- "lecture_outputs/teacher_answers.json"

Instructions: 
# Come up with some simple rules to encrypt the sentence.
# Modify the "encrypt_sentence" function in the teacher script to encrypt the sentence.
# Humans should verify that the output examples are unambiuous.
# Please thoroughly check the outputs before proceeding to "step02_full_convo.py"

Rules applied:
--------------------- ** FILL IN BELOW ** ------------------




------------------ NOTES END HERE ------------------------'''

import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    
    # Rule 1: Remove the last noun (singular or plural) from the sentence
    # Rule 2: Append the reversed last noun to the end of the sentence
    last_noun = ''
    last_noun_index = -1
    for i, (word, tag) in enumerate(tagged_words):
        if tag.startswith('NN'):
            last_noun = word
            last_noun_index = i
    
    # Remove the last noun from the sentence
    if last_noun_index >= 0:
        words.pop(last_noun_index)
    
    # Construct the new sentence without the last noun
    new_sentence = ' '.join(words)
    
    # Append the reversed last noun to the end of the sentence
    new_sentence = new_sentence.strip()
    if new_sentence[-1] == '.':
        new_sentence = new_sentence[:-1] + last_noun[::-1] + '.'
    else:
        new_sentence += ' ' + last_noun[::-1]
    
    return new_sentence

# Examples
examples = [
    "The cat sat on the mat.",
    "Knowledge speaks louder than words.",
    "A shiny and brown fox jumps over the lazy rainbow.",
    "The quick brown fox jumps over the lazy turtle.",
    "I prefer guacamole over hummus.",
    "You are doing a lot of work this weekend."
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))

# Save the list to JSON
with open(f"teacher_examples.json", "w", encoding='utf-8') as json_file:
    json.dump(examples, json_file)

with open(f"teacher_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)

print(f"Examples: \n{examples}" + "\n")
print(f"Answers: \n{answers}" + "\n")

print("SUCCESS: teacher json files created.")
