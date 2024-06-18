import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def to_camel_case(word):
    return word[0].upper() + word[1:] if word else word

def encrypt_sentence(sentence):
    # Convert the entire sentence to lowercase
    sentence = sentence.lower()
    
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
        
    # Tokenize and tag the sentence
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    
    # Dictionary for word substitution
    word_substitution = {
        'the': '',
        'dog': 'ofi',
        'cat': 'kowi',
        'chases': 'lhiyoh',
        'stinks': 'shoha',
        'woman': 'ihoo',
        'loves': 'hollo',
        'man': 'hattak',
        'i': 'lhiyohl',
        'me': 'salhiyoh',
        'he': 'hil',
        'she': 'hil',
        'dances': 'hilha'
    }
    
    # Encrypted words list
    encrypted_words = []
    
    # Encrypt the sentence
    for word, tag in tagged_words:
        encrypted_word = word_substitution.get(word, word)
        if tag.startswith('NN'):  # Noun
            encrypted_word += 'at'
        elif tag.startswith('VB'):  # Verb
            encrypted_word += 'li'
        elif word == 'i':  # Special case for 'I'
            encrypted_word += 'lili'
        elif word in ['he', 'she']:  # Special case for 'he'/'she'
            encrypted_word = 'sa' + encrypted_word + 'li'
        encrypted_words.append(encrypted_word)
    
    # Remove empty strings
    encrypted_words = [word for word in encrypted_words if word]
    
    # Convert the first letter to uppercase
    encrypted_words[0] = to_camel_case(encrypted_words[0])
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ' '.join(encrypted_words) + '.'
    
    return new_sentence

# Examples
examples = [
    "The dog chases the cat.",
    "The cat chases the dog.",
    "The dog stinks.",
    "The woman loves the man.",
    "I chase him.",
    "He chases me.",
    "She dances."
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))

# Save the list to JSON
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)