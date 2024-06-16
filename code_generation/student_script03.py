import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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
        new_sentence = new_sentence[:-1] + ' ' + last_noun[::-1] + '.'
    else:
        new_sentence += ' ' + last_noun[::-1]
    
    return new_sentence

# Examples
examples = [
    "The cat sat on the mat.",
    "Knowledge speaks louder than words.",
    "A shiny and brown fox jumps over the lazy dog.",
    "The sun and moon and stars all rise in the east.",
    "The big big belly is full.",
    "Failure is the mother of sucess."
]

for example in examples:
    print(encrypt_sentence(example))
