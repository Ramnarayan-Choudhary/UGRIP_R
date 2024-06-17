import json
from nltk import pos_tag
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    words = word_tokenize(sentence)
    new_words = []
    
    for word in words:
        # Rule 1: Words with a certain length (possibly 3 or more letters) are reversed.
        # Rule 3: The last word in the sentence is reversed.
        if len(word) >= 3 and word not in [".", ",", "!", "?"]:
            # Exclude punctuation from being reversed
            if word[-1] in ".,;!?":
                new_word = word[:-1][::-1] + word[-1]
            else:
                new_word = word[::-1]
        else:
            new_word = word
        new_words.append(new_word)
    
    # Rule 3: The last word in the sentence is reversed (correcting for punctuation).
    if new_words[-2][-1] in ".,;!?":
        new_words[-2] = new_words[-2][:-1][::-1] + new_words[-2][-1]
    
    new_sentence = ' '.join(new_words)
    # Fix spacing issues with punctuation
    new_sentence = new_sentence.replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?").replace(" ;", ";")
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