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
        
    # Tokenize the sentence
    words = word_tokenize(sentence)
    
    # Mapping of English words to their encrypted counterparts
    word_mapping = {
        'the': '',
        'dog': "ofi'at",
        'cat': "kowi'at",
        'chases': 'lhiyohli',
        'stinks': 'shoha',
        'woman': "ihooat",
        'loves': 'hollo',
        'man': "hattakã",
        'i': 'lhiyohlili',
        'me': 'salhiyohli',
        'he': 'sa',
        'she': 'sa',
        'dances': 'hilha'
    }
    
    # Encrypt the words using the mapping
    encrypted_words = []
    for word in words:
        encrypted_word = word_mapping.get(word, word)
        encrypted_words.append(encrypted_word)
    
    # Remove empty strings resulting from 'the' mapping to ''
    encrypted_words = [word for word in encrypted_words if word]
    
    # Special handling for pronouns and their actions
    if sentence in ['i chase him', 'i chase her']:
        encrypted_words = ['lhiyohlili']
    elif sentence in ['he chases me', 'she chases me']:
        encrypted_words = ['salhiyohli']
    elif sentence in ['he dances', 'she dances']:
        encrypted_words = ['hilha']
    
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