from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    
    # Rule 1: Remove the first noun from the sentence
    # Rule 2: Append the reversed first noun to the end of the sentence
    first_noun = ''
    for word, tag in tagged_words:
        if tag.startswith('NN') and first_noun == '':
            first_noun = word
            words.remove(word)
            break
    
    new_sentence = ' '.join(words) + ' ' + first_noun[::-1]
    new_sentence = new_sentence.strip()
    if new_sentence[-1] == '.':
        new_sentence = new_sentence[:-1] + first_noun[::-1] + '.'
    else:
        new_sentence += first_noun[::-1]
    
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
