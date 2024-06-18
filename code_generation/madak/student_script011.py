import json
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    # Remove dot
    if sentence[-1] == '.':
        sentence = sentence[:-1]
    
    # Tokenize the sentence
    words = word_tokenize(sentence)
    
    # Define the encryption rules based on the provided examples
    word_to_encrypted = {
        'the': '', 'whole': 'vatbung', 'world': 'menemen',
        'many': 'ax', 'eyes': 'angkatli', 'vines': 'anoos',
        'fire': 'ao', 'big': 'empa', 'songs': 'ngkompixan',
        'hearts': 'vempeve', 'days': 'venaleng', 'places': 'vengkot',
        'villages': 'venmenemen', 'singing': 'vixan', 'spirit': 'roonan',
        'hot': 'xongkao', 'coal': 'xongkao', 'ember': 'xongkao', 'part': 'xontaamang',
        'of': 'xontaamang', 'a': 'xontaamang', 'garden': 'xontaamang',
        'two': 'u', 'group': 'bungtadi', 'men': 'tadi',
        'brothers': 'neton', 'sisters': 'neton', 'grandchild': 'rubuno',
        'tree': 'una', 'things': 'vanga', 'white': 'xavus'
    }
    
    # Define the prefix rule based on the number of words in the original sentence
    num_words = len(words)
    if num_words == 1:
        prefix = 'la'
    elif num_words == 2:
        prefix = 'lu'
    elif num_words == 3:
        prefix = 'le'
    else:
        prefix = 'lo'
    
    # Encrypt the words using the predefined rules
    encrypted_words = [word_to_encrypted.get(word.lower(), word.lower()) for word in words]
    
    # Join the prefix and the encrypted words into a single string
    new_sentence = prefix + ''.join(encrypted_words)
    
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