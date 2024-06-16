import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def encrypt_sentence(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    
    # Rule 1: Remove the first noun (singular or plural) from the sentence
    # Rule 2: Append the reversed first noun to the end of the sentence
    # Note: Adjectives (JJ) that directly precede a noun should also be removed along with the noun
    first_noun_index = None
    for i, (word, tag) in enumerate(tagged_words):
        if tag in ('NN', 'NNS') and first_noun_index is None:
            first_noun_index = i
            break
    
    # Check if there is an adjective before the noun and remove it as well
    if first_noun_index is not None and tagged_words[first_noun_index - 1][1] == 'JJ':
        first_noun_index -= 1
    
    # Extract the noun (and adjective if applicable) and reverse it
    noun_phrase = ' '.join(word for word, tag in tagged_words[first_noun_index:first_noun_index + 2])
    reversed_noun_phrase = noun_phrase[::-1]
    
    # Construct the new sentence without the noun phrase
    new_sentence = ' '.join(word for i, (word, tag) in enumerate(tagged_words) if i < first_noun_index or i > first_noun_index + 1)
    
    # Append the reversed noun phrase to the end of the sentence
    new_sentence = new_sentence.strip()
    if new_sentence[-1] == '.':
        new_sentence = new_sentence[:-1] + ' ' + reversed_noun_phrase + '.'
    else:
        new_sentence += ' ' + reversed_noun_phrase
    
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