import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    words = sentence.split()
    if words:
        words[-1] = words[-1][::-1]
    new_sentence = ' '.join(words)
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
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)