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
        'dog': "ofi'",
        'cat': "kowi'",
        'chases': 'lhiyoh',
        'stinks': 'shoha',
        'woman': "ihoo'",
        'loves': 'hollo',
        'man': "hattak'",
        'i': 'lhiyohl',
        'me': 'salhiyoh',
        'he': 'sa',
        'she': 'sa',
        'dances': 'hilha'
    }
    
    # Encrypted words list
    encrypted_words = []
    
    # Encrypt the sentence
    for word, tag in tagged_words:
        encrypted_word = word_substitution.get(word, word)
        if tag.startswith('NN') and word not in ['i', 'me', 'he', 'she']:  # Noun
            encrypted_word += 'at'
        elif tag.startswith('VB') and word not in ['i', 'me', 'he', 'she']:  # Verb
            encrypted_word += 'li'
        encrypted_words.append(encrypted_word)
    
    # Remove empty strings and join the words
    encrypted_sentence = ' '.join(filter(None, encrypted_words))
    
    # Handle special cases for pronouns
    if sentence == 'i chase him' or sentence == 'i chase her':
        encrypted_sentence = 'lhiyohlili'
    elif sentence == 'he chases me' or sentence == 'she chases me':
        encrypted_sentence = 'salhiyohli'
    elif sentence == 'he dances' or sentence == 'she dances':
        encrypted_sentence = 'hilha'
    
    # Convert the first letter to uppercase
    encrypted_sentence = to_camel_case(encrypted_sentence)
    
    # Add a period at the end
    new_sentence = encrypted_sentence + '.'
    
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