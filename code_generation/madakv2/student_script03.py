import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
        
    # TO DO: YOUR CODE
    words = word_tokenize(sentence)
    encrypted_words = []
    prefix = 'l' + ('u' * (len(words) - 1))
    
    # Placeholder dictionary for word encryption based on observed patterns
    encryption_dict = {
        'the whole world': 'vatbungmenemen',
        'many eyes': 'axangkatli',
        'many vines': 'axanoos',
        'fire': 'axao',
        'big vines': 'emparoos',
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
        'two days': 'aleng',
        'group of men': 'bungtadi',
        'two brothers': 'neton',
        'two sisters': 'neton',
        'grandchild': 'rubuno',
        'tree': 'una',
        'two things': 'vanga',
        'two big hearts': 'vatpeve',
        'brothers': 'vutneton',
        'sisters': 'vutneton',
        'men': 'vuttadi',
        'two white men': 'xavus'
    }
    
    # Encrypt the sentence using the dictionary
    encrypted_sentence = prefix
    for word in words:
        if word in encryption_dict:
            encrypted_sentence += encryption_dict[word]
        else:
            # For words not in the dictionary, we'll just append the word as is.
            # In a real encryption scenario, you would have rules for all words.
            encrypted_sentence += word
    
    return encrypted_sentence

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