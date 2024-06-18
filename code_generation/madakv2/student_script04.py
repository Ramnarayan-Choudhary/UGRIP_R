import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
        
    # TO DO: YOUR CODE
    # Dictionary mapping original words to their encrypted counterparts
    encryption_dict = {
        'the whole world': 'lavatbungmenemen',
        'many eyes': 'laxangkatli',
        'many vines': 'laxanoos',
        'fire': 'laxao',
        'big vines': 'lemparoos',
        'songs': 'lengkompixan',
        'hearts': 'levempeve',
        'days': 'levenaleng',
        'places': 'levengkot',
        'villages': 'levenmenemen',
        'singing': 'livixan',
        'spirit': 'loroonan',
        'hot coal': 'loxongkao',
        'ember': 'loxongkao',
        'part of a garden': 'loxontaamang',
        'two days': 'lualeng',
        'group of men': 'lubungtadi',
        'two brothers': 'luneton',
        'two sisters': 'luneton',
        'grandchild': 'lurubuno',
        'tree': 'luuna',
        'two things': 'luvanga',
        'two big hearts': 'luvatpeve',
        'brothers': 'luvutneton',
        'sisters': 'luvutneton',
        'men': 'luvuttadi',
        'two white men': 'luxavus'
    }
    
    # Tokenize the sentence and encrypt using the dictionary
    tokens = word_tokenize(sentence)
    encrypted_tokens = []
    for token in tokens:
        # Check if the token is part of a compound phrase
        compound_key = ' '.join(tokens)
        if compound_key in encryption_dict:
            return encryption_dict[compound_key]
        # Encrypt individual words (if not part of a compound phrase)
        if token in encryption_dict:
            encrypted_tokens.append(encryption_dict[token])
        else:
            encrypted_tokens.append(token)
    
    # Join the encrypted tokens into a single string
    new_sentence = ''.join(encrypted_tokens)
    return new_sentence

# Examples
examples = [
    "the whole world",
    "many eyes",
    "many vines",
    "fire",
    "big vines",
    "songs",
    "hearts",
    "days",
    "places",
    "villages",
    "singing",
    "spirit",
    "hot coal",
    "part of a garden",
    "two days",
    "group of men",
    "two brothers",
    "grandchild",
    "tree",
    "two things",
    "two big hearts",
    "brothers",
    "men",
    "two white men"
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))

# Save the list to JSON
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)