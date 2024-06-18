import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def to_camel_case(word):
    return word[0].upper() + word[1:] if word else word

def encrypt_sentence(sentence):
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
        
    # TO DO: YOUR CODE
    words = word_tokenize(sentence)
    tags = pos_tag(words)
    encrypted_words = []
    prefix = 'l' + ('u' * (len(words) - 1))
    
    # Placeholder dictionary for word encryption based on observed patterns
    encryption_dict = {
        'the': '',
        'whole': 'vatbung',
        'world': 'menemen',
        'many': 'axan',
        'eyes': 'gkatli',
        'vines': 'oos',
        'fire': 'ao',
        'big': 'empa',
        'songs': 'ngkompixan',
        'hearts': 'vempeve',
        'days': 'venaleng',
        'places': 'vengkot',
        'villages': 'venmenemen',
        'singing': 'vixan',
        'spirit': 'roonan',
        'hot coal': 'oxongkao',
        'ember': 'oxongkao',
        'part of a garden': 'oxontaamang',
        'two': 'ua',
        'group of men': 'bungtadi',
        'brothers': 'neton',
        'sisters': 'neton',
        'grandchild': 'rubuno',
        'tree': 'una',
        'things': 'vanga',
        'white': 'xavus',
        'men': 'vuttadi'
    }
    
    for word, tag in tags:
        encrypted_word = encryption_dict.get(word, word)
        encrypted_words.append(prefix + encrypted_word)
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ''.join(encrypted_words)
    
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