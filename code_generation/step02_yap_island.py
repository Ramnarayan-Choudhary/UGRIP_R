from nltk import pos_tag
from nltk.tokenize import word_tokenize
# Exact same prompt

# Passed into GPT-3.5 Turbo:
def encrypt_sentence(sentence):
    words = sentence.split()
    encrypted_words = []
    for word in words:
        encrypted_word = word[::-1]
        encrypted_words.append(encrypted_word)
    encrypted_sentence = ' '.join(encrypted_words)
    return encrypted_sentence

# original_sentence = "I am learning Python"
# print(encrypt_sentence(original_sentence))

# original_sentence = "We eat pizza."
# print(encrypt_sentence(original_sentence))

# original_sentence = "He drinks coffee."
# print(encrypt_sentence(original_sentence))


# Passed into GPT-4:
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def encrypt_sentence(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Tag parts of speech
    tagged_words = pos_tag(words)
    
    # Find the first noun in the sentence as the subject
    subject = None
    for word, tag in tagged_words:
        if is_noun(tag):
            subject = word
            break
    
    if not subject:
        raise ValueError("No subject noun found in the sentence.")
    
    # Reverse the subject
    reversed_subject = subject[::-1]
    
    # Remove the subject from its original position
    words.remove(subject)
    
    # Construct the new sentence with the reversed subject at the end
    new_sentence = ' '.join(words[:-1]) + ' ' + reversed_subject + '.'
    
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
   

'''

# Example usage:
original_sentence = "The cat sat on the mat."
print("Original Sentence: " + original_sentence + "\n" + 
      "Engrypted Sentence: " + reverse_subject(original_sentence) + "\n")

original_sentence = "Knowledge speaks louder than words."
print("Original Sentence: " + original_sentence + "\n" + 
      "Engrypted Sentence: " + reverse_subject(original_sentence) + "\n")

original_sentence = "A shiny and brown fox jumps over the lazy dog."
print("Original Sentence: " + original_sentence + "\n" + 
      "Engrypted Sentence: " + reverse_subject(original_sentence) + "\n")

original_sentence = "The sun and moon and stars all rise in the east."
print("Original Sentence: " + original_sentence + "\n" + 
      "Engrypted Sentence: " + reverse_subject(original_sentence) + "\n")

original_sentence = "The big big belly is full."
print("Original Sentence: " + original_sentence + "\n" + 
      "Engrypted Sentence: " + reverse_subject(original_sentence) + "\n")

original_sentence = "Failure is the mother of sucess."
print("Original Sentence: " + original_sentence + "\n" + 
      "Engrypted Sentence: " + reverse_subject(original_sentence) + "\n")

      '''
# Tokenize the sentence into words
bool_debug = False
if bool_debug: 
    original_sentence = "The big big belly is full."
    words = word_tokenize(original_sentence)
    # Tag parts of speech
    tagged_words = pos_tag(words)

    # Find the first noun in the sentence as the subject
    subject = None
    for word, tag in tagged_words:
        if is_noun(tag):
            subject = word
            break

    if not subject:
        raise ValueError("No subject noun found in the sentence.")

    # Reverse the subject
    reversed_subject = subject[::-1]

    # Remove the subject from its original position
    words.remove(subject)

    # Construct the new sentence with the reversed subject at the end
    new_sentence = ' '.join(words[:-1]) + ' ' + reversed_subject + '.'
    