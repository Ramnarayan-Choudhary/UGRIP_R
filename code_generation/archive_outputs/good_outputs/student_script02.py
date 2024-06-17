import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    # Split the sentence into words
    words = sentence.split()
    # Check if there are any words in the sentence
    if words:
        # Remove punctuation from the last word if present
        last_word = words[-1].rstrip('.!?')
        # Reverse the last word and add back the punctuation if it was removed
        last_word = last_word[::-1] + (words[-1][-1] if words[-1][-1] in '.!?' else '')
        # Replace the last word in the list with the reversed word
        words[-1] = last_word
    # Reconstruct the sentence
    new_sentence = ' '.join(words)
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
with open("student_answers.json", "w", encoding='utf-8') as json_file:
    json.dump(answers, json_file)
print(answers)