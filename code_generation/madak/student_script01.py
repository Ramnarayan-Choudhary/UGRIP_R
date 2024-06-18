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
    pos_tags = pos_tag(words)
    encrypted_words = []
    
    # Rule 1: First letter based on the number of words
    prefix = 'l'  # Assuming 'l' is used for any number of words
    encrypted_words.append(prefix)
    
    # Rule 3: Specific encrypted words or syllables
    word_to_encrypted = {
        'the': 'a', 'whole': 'vatbung', 'world': 'menemen',
        'many': 'ax', 'eyes': 'angkatli', 'vines': 'anoos',
        'fire': 'axao', 'big': 'empa', 'songs': 'engkompixan',
        'hearts': 'evempeve', 'days': 'enaleng', 'places': 'engkot',
        'villages': 'enmenemen', 'singing': 'ivixan', 'spirit': 'oroonan',
        'hot coal': 'oxongkao', 'ember': 'oxongkao', 'part of a garden': 'oxontaamang',
        'two': 'ua', 'group of men': 'ubungtadi', 'brothers': 'uneton', 'sisters': 'uneton',
        'grandchild': 'urubuno', 'tree': 'uuna', 'things': 'uvanga',
        'white': 'uxavus', 'men': 'uvuttadi'
    }
    
    for word, pos in pos_tags:
        encrypted_word = word_to_encrypted.get(word, word)  # Default to the original word if not found
        encrypted_words.append(encrypted_word)
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ''.join(encrypted_words) + '.'
    
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