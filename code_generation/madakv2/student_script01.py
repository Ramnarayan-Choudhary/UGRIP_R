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
    
    for word, tag in tags:
        # This is a placeholder for the actual encryption logic
        # which is not provided due to the lack of clear rules.
        # The following line should be replaced with the actual
        # encryption rules once they are determined.
        encrypted_word = prefix + word  # Placeholder
        encrypted_words.append(encrypted_word)
    
    # Join the words back into a sentence and add a period at the end
    new_sentence = ' '.join(encrypted_words) + '.'
    
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
    "(hot coal/ember)",
    "part of a garden",
    "two days",
    "group of men",
    "two brothers; two sisters",
    "grandchild",
    "tree",
    "two things",
    "two big hearts",
    "brothers; sisters",
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