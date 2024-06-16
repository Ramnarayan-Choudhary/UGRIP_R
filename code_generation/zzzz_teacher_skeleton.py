
import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(example):

    # TODO: using the nltk module, construct the "new_sentence" that can encrypt each sentence from "examples".
    new_sentence = example[::-1]

    return new_sentence

# Examples
examples = [
    "The cat sat on the mat.",
    "Knowledge speaks louder than words.",
    "A shiny and brown fox jumps over the lazy dog.",
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))
    
# Save the list to JSON
with open(f"ansewrs.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)

