import json
import re

def noun_scrambler(text, replacements):
    def replacer(match):
        return replacements[match.group(0)]

    pattern = re.compile("|".join(map(re.escape, replacements.keys())))
    return pattern.sub(replacer, text)

# Load JSON data from a file
with open('input.json', 'r') as file:
    data = json.load(file)

# Noun replacements dictionary
scramble_dict = {"cat": "dog", "dog": "woman", "woman": "cat"}

# Replace nouns in the "train" field
if 'train' in data:
    data['train'] = [noun_scrambler(sentence, scramble_dict) for sentence in data['train']]

# Save the modified JSON data back to a file
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)


