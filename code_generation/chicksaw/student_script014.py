import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Mapping of words to their encrypted forms
word_mapping = {
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

# Special cases for pronouns
pronoun_mapping = {
    'i': "lhiyohlili",
    'me': "salhiyohli",
    '(he/she)': "salhiyohli",
    '(him/her)': "lhiyohlili"
}

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
    
    # Encrypt the words based on the mapping
    encrypted_words = []
    for word in words:
        if word in word_mapping:
            encrypted_word = word_mapping[word]
        elif word in pronoun_mapping:
            encrypted_word = pronoun_mapping[word]
        else:
            encrypted_word = word  # This case should not happen with the given examples
        encrypted_words.append(encrypted_word)
    
    # Remove empty strings (which represent 'the' in the original sentence)
    encrypted_words = [word for word in encrypted_words if word]
    
    # Special handling for pronouns in parentheses
    if '(he/she)' in sentence:
        encrypted_words = [pronoun_mapping['(he/she)'] if 'sa' in word else word for word in encrypted_words]
    if '(him/her)' in sentence:
        encrypted_words = [pronoun_mapping['(him/her)'] if 'ã' in word else word for word in encrypted_words]
    
    # Capitalize the first letter of the encrypted sentence
    encrypted_words[0] = to_camel_case(encrypted_words[0])
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ' '.join(encrypted_words) + '.'
    
    return new_sentence

# Examples
examples = [
    'The dog chases the cat.',
    'The cat chases the dog.',
    'The dog stinks.',
    'The woman loves the man.',
    'I chase (him/her).',
    '(He/She) chases me.',
    '(He/She) dances.'
]

# Encrypt each example sentence
answers = [encrypt_sentence(example) for example in examples]

# Save the list to JSON
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)

# Output the answers
print(answers)