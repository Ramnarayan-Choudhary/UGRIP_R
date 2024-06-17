import json
from nltk.tokenize import word_tokenize

def encrypt_sentence(sentence):
    words = word_tokenize(sentence)
    new_words = []
    for word in words:
        # Check if the word has an odd number of letters and contains only alphabets
        if len(word) % 2 != 0 and word[-1].isalpha():
            new_word = word[::-1]  # Reverse the word
        elif len(word) % 2 != 0 and not word[-1].isalpha():
            # Reverse the word except for the last character (punctuation)
            new_word = word[:-1][::-1] + word[-1]
        else:
            new_word = word  # Keep the word unchanged
        new_words.append(new_word)
    new_sentence = ' '.join(new_words)
    # Correct the spacing around punctuation
    new_sentence = new_sentence.replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?")
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