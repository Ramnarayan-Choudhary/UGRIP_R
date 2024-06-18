import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Dictionary mapping English words to their encrypted counterparts
encryption_dict = {
    'the': '',
    'dog': "ofi'at",
    'cat': "kowi'at",
    'chases': "lhiyohli",
    'stinks': "shoha",
    'woman': "ihooat",
    'loves': "hollo",
    'man': "hattakã",
    'i': "lhiyohlili",
    'me': "salhiyohli",
    'dances': "hilha",
    '(he/she)': "sa",
    '(him/her)': "ã"
}

def to_camel_case(word):
    return word[0].upper() + word[1:] if word else word

def encrypt_sentence(sentence):
    # Convert the entire sentence to lowercase
    sentence = sentence.lower()
    
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
        
    # TO DO: YOUR CODE
    words = word_tokenize(sentence)
    tags = pos_tag(words)
    encrypted_words = []
    for word, tag in zip(words, tags):
        encrypted_word = encryption_dict.get(word, word)
        if tag[1].startswith('VB'):
            encrypted_word = encrypted_word.rstrip('li')  # Verbs already have 'li' in the dictionary
        elif tag[1].startswith('NNP'):
            encrypted_word = encrypted_word.rstrip('at')  # Proper nouns do not get 'at'
        encrypted_words.append(encrypted_word)
    
    # Handle special cases for pronouns
    if '(he/she)' in sentence:
        encrypted_words = ['salhiyohli' if word == 'sa' else word for word in encrypted_words]
    if '(him/her)' in sentence:
        encrypted_words = ['lhiyohlili' if word == 'ã' else word for word in encrypted_words]
    
    # Remove empty strings and capitalize the first letter of the sentence
    encrypted_words = [word for word in encrypted_words if word]
    encrypted_words[0] = to_camel_case(encrypted_words[0])
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ' '.join(encrypted_words).replace(' .', '.') + '.'
    
    return new_sentence

# Examples
examples = ['The dog chases the cat.',
 'The cat chases the dog.',
 'The dog stinks.',
 'The woman loves the man.',
 'I chase (him/her).',
 '(He/She) chases me.',
 '(He/She) dances.'
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))

# Save the list to JSON
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)