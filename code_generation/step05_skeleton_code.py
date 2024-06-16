

'''
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def decrypt_sentence(sentence):
   
    # TODO: using the nltk module, construct the "new_sentence" that can simulate the examples given, then decrypt the input sentence.
    
    return new_sentence
'''
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def encrypt_sentence(sentence):
    # Split the sentence and keep track of the period if present
    if sentence.endswith('.'):
        sentence = sentence[:-1]
        period = '.'
    else:
        period = ''
    
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)

    # Find the first noun (NN, NNS, NNP, NNPS)
    first_noun_index = None
    for i, (word, pos) in enumerate(pos_tags):
        if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
            first_noun_index = i
            break

    if first_noun_index is not None:
        # Extract the first noun
        first_noun = words[first_noun_index]
        # Remove the first noun from its original position
        words.pop(first_noun_index)
        # Reverse the first noun and add it to the end
        words.append(first_noun[::-1])

    # Join the words to form the new sentence and reattach the period if present
    new_sentence = ' '.join(words) + period
    return new_sentence


def encrypt_sentence_old(sentence):
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)

    # Find the first noun (NN, NNS, NNP, NNPS)
    first_noun_index = None
    for i, (word, pos) in enumerate(pos_tags):
        if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
            first_noun_index = i
            break

    if first_noun_index is not None:
        # Extract the first noun
        first_noun = words[first_noun_index]
        # Remove the first noun from its original position
        words.pop(first_noun_index)
        # Reverse the first noun and add it to the end
        words.append(first_noun[::-1])

    # Join the words to form the new sentence
    new_sentence = ' '.join(words)
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
    print("Original Sentence:", example)
    print("Encrypted Sentence:", encrypt_sentence(example))
    print()



# Examples
examples = [
    "The cat sat on the mat.",
    "Knowledge speaks louder than words.",
    "A shiny and brown fox jumps over the lazy dog.",
    "The sun and moon and stars all rise in the east.",
    "The big big belly is full.",
    "Failure is the mother of sucess."
]

print("My original sentences: ")
for i, example in enumerate(examples):
    print("Sentence " + str(i+1) + ": " + example)


print("My answers: ")
for i, example in enumerate(examples):
    print("Sentence " + str(i+1) + ": " + encrypt_sentence(example))


print("My students' answers: ")
for i, example in enumerate(examples):
    print("Sentence " + str(i+1) + ": " + encrypt_sentence_old(example))

