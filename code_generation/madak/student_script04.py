import json
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
        
    # TO DO: YOUR CODE
    words = word_tokenize(sentence)
    encrypted_words = []
    
    # Rule 1: First letter based on the number of words
    num_words = len(words)
    if num_words == 1:
        first_letter = 'laxa'  # Placeholder for one-word sentences
    elif num_words == 2:
        first_letter = 'lua'  # Placeholder for two-word sentences
    elif num_words == 3:
        first_letter = 'le'  # Placeholder for three-word sentences
    else:
        first_letter = 'lo'  # Placeholder for sentences with four or more words
    encrypted_words.append(first_letter)
    
    # Rule 3: Specific encrypted words or syllables
    word_to_encrypted = {
        'the': '', 'whole': 'vatbung', 'world': 'menemen',
        'many': 'x', 'eyes': 'angkatli', 'vines': 'anoos',
        'fire': 'ao', 'big': 'mpa', 'songs': 'ngkompixan',
        'hearts': 'vempeve', 'days': 'venaleng', 'places': 'vengkot',
        'villages': 'venmenemen', 'singing': 'vixan', 'spirit': 'roonan',
        'hot': 'xongkao', 'coal': 'xongkao', 'ember': 'xongkao', 'part': 'xontaamang',
        'of': 'xontaamang', 'a': 'xontaamang', 'garden': 'xontaamang',
        'two': 'u', 'group': 'bungtadi', 'men': 'tadi',
        'brothers': 'neton', 'sisters': 'neton', 'grandchild': 'rubuno',
        'tree': 'una', 'things': 'vanga', 'white': 'xavus'
    }
    
    # Apply encryption rules
    for word in words:
        encrypted_word = word_to_encrypted.get(word.lower(), '')
        encrypted_words.append(encrypted_word)
    
    # Join the words into a sentence without spaces or a period at the end
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