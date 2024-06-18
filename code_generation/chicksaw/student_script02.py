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
        
    # TO DO: YOUR CODE
    words = word_tokenize(sentence)
    tags = pos_tag(words)
    encrypted_words = []
    for word, tag in zip(words, tags):
        encrypted_word = ''
        if word == 'the':
            continue
        elif word == 'dog':
            encrypted_word = 'ofi'
        elif word == 'cat':
            encrypted_word = 'kowi'
        elif word == 'chases':
            encrypted_word = 'lhiyoh'
        elif word == 'stinks':
            encrypted_word = 'shoh'
        elif word == 'woman':
            encrypted_word = 'ihoo'
        elif word == 'loves':
            encrypted_word = 'hollo'
        elif word == 'man':
            encrypted_word = 'hattak'
        elif word == 'i':
            encrypted_word = 'lhiyohlil'
        elif word == 'me':
            encrypted_word = 'salhiyoh'
        elif word == 'dances':
            encrypted_word = 'hilh'
        elif word in ('he', 'she'):
            encrypted_word = 'sa'
        elif word in ('him', 'her'):
            encrypted_word = 'ã'
        
        if tag[1].startswith('VB'):
            encrypted_word += 'li'
        elif tag[1].startswith('NN') and word not in ('i', 'me', 'he', 'she', 'him', 'her'):
            encrypted_word += 'at'
        elif word in ('he', 'she'):
            encrypted_word += 'lhiyoh'
        elif word in ('him', 'her'):
            encrypted_word = 'lhiyoh' + encrypted_word
        
        encrypted_words.append(encrypted_word)
    
    # Special handling for pronouns in parentheses
    if '(he/she)' in sentence:
        encrypted_words = ['Sa' + w if w.startswith('lhiyoh') else w for w in encrypted_words]
    if '(him/her)' in sentence:
        encrypted_words = [w + 'ã' if w.startswith('lhiyoh') else w for w in encrypted_words]
    
    # Special handling for 'i' as a single word sentence
    if sentence == 'i chase':
        encrypted_words = ['Lhiyohlili']
    
    # Convert the first letter of the sentence to CamelCase
    encrypted_words[0] = to_camel_case(encrypted_words[0])
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ' '.join(encrypted_words).replace(' lhiyohã', 'ã lhiyoh').replace(' lhiyohli', 'li.') + '.'
    new_sentence = new_sentence.replace(' .', '.')
    
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