import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import json

nltk.download('averaged_perceptron_tagger')

def encrypt_sentence(example):
    words = word_tokenize(example)
    pos_tags = pos_tag(words)
    
    new_words = []
    for word, tag in pos_tags:
        # Rule 1: Reverse the word if it's the last word in the sentence.
        # Rule 2: Reverse the word if it's a noun (NN, NNP, NNS, NNPS) but not the first word.
        if word == words[-1].rstrip('.?!'):
            new_words.append(word[::-1])
        elif tag in ['NN', 'NNS', 'NNP', 'NNPS'] and new_words:
            new_words.append(word[::-1])
        else:
            new_words.append(word)
    
    new_sentence = ' '.join(new_words)
    # Fix punctuation spacing
    new_sentence = new_sentence.replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?')
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
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)

print(answers)
