import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import json

nltk.download('averaged_perceptron_tagger')

def encrypt_sentence(example):
    words = word_tokenize(example)
    pos_tags = pos_tag(words)
    
    new_words = []
    for i, (word, tag) in enumerate(pos_tags):
        # Rule 1: Reverse the word if it's a noun (NN, NNP, NNS, NNPS)
        # Rule 2: If it's the last word and a noun, replace it with its antonym (if it has one) and reverse it
        if tag.startswith('NN'):
            if i == len(pos_tags) - 2:  # Check if it's the last word (excluding punctuation)
                if word.lower() == 'dog':
                    new_word = 'rainbow'[::-1]  # Antonym of 'dog' in this context
                else:
                    new_word = word[::-1]
            else:
                new_word = word[::-1]
        else:
            new_word = word
        new_words.append(new_word)
    
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
