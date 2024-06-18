import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Dictionary for word substitution
word_substitution = {
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
    encrypted_words = []
    for word in words:
        if word in word_substitution:
            encrypted_word = word_substitution[word]
        elif word in ('he', 'she'):
            encrypted_word = 'sa'
        elif word in ('him', 'her'):
            encrypted_word = 'ã'
        else:
            encrypted_word = word

        encrypted_words.append(encrypted_word)

    # Handling special cases for pronouns
    if 'i' in encrypted_words:
        encrypted_words = ['lhiyohlili' if word == 'i' else word for word in encrypted_words]
    if 'me' in encrypted_words:
        encrypted_words = ['salhiyohli' if word == 'me' else word for word in encrypted_words]
    if 'ã' in encrypted_words:
        encrypted_words = ['lhiyohlili' if word == 'ã' else word for word in encrypted_words]
    if 'sa' in encrypted_words:
        encrypted_words = ['salhiyohli' if word == 'sa' else word for word in encrypted_words]

    # Remove empty strings and capitalize the first letter of the sentence
    encrypted_words = [word for word in encrypted_words if word]
    encrypted_words[0] = to_camel_case(encrypted_words[0])
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ' '.join(encrypted_words).replace(' .', '.').replace('lhiyohli.', 'lhiyohli') + '.'
    
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