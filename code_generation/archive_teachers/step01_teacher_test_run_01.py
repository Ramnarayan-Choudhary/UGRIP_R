import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    
    # Rule 1: Remove the last noun (singular or plural) from the sentence
    # Rule 2: Append the reversed last noun to the end of the sentence
    # Additional Rule: Reverse the spelling of adjectives in the sentence
    last_noun = ''
    last_noun_index = -1
    for i, (word, tag) in enumerate(tagged_words):
        if tag.startswith('JJ'):
            # Reverse the spelling of adjectives
            words[i] = word[::-1]
        if tag.startswith('NN'):
            last_noun = word
            last_noun_index = i
    
    # Remove the last noun from the sentence
    if last_noun_index >= 0:
        words.pop(last_noun_index)
    
    # Construct the new sentence without the last noun
    new_sentence = ' '.join(words)
    
    # Append the reversed last noun to the end of the sentence
    new_sentence = new_sentence.strip()
    if new_sentence[-1] == '.':
        new_sentence = new_sentence[:-1] + last_noun[::-1] + '.'
    else:
        new_sentence += ' ' + last_noun[::-1]
    
    return new_sentence

# Examples
examples = [
    "The cat sat on the mat.",
    "Knowledge speaks louder than words.",
    "A shiny and brown fox jumps over the lazy rainbow.",
    "The quick brown fox jumps over the lazy turtle.",
    "I prefer guacamole over hummus.",
    "You are doing a lot of work this weekend."
]

answers = []
for example in examples:
    answers.append(encrypt_sentence(example))

# Save the list to JSON
with open("teacher_examples.json", "w", encoding='utf-8') as json_file:
    json.dump(examples, json_file)

with open("teacher_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)

print(f"Examples: \n{examples}\n")
print(f"Answers: \n{answers}\n")

print("SUCCESS: teacher json files created.")
