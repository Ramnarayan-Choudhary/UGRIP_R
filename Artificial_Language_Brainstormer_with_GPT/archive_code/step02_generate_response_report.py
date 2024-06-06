

def load_file_as_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def fill_responses_in_text(text_content, responses):
    for i in range(len(responses)):
        placeholder = f'[insert respone {i+1}]'
        text_content = text_content.replace(placeholder, responses[i])
    return text_content

def save_conversation_to_file(text_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text_content)
    print(f"Conversation saved to {output_file}")


# Example usage:
txt_content = load_file_as_string('input.txt')

responses = [
    "Alphabet: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T",
    "Translations: Cáin (dog), Siál (thirsty), Rát (chases), Peipir (paper), Líil (yellow), Híiménz (humans)",
    "Translations:\n- Cáin cén Líil.\n- Peipir disépírded énd térnd Líil.\n- Híiménz dón't yúzhúlli chéis Cáin.\n- Peipir dósnt gét Siál."
]

output_text = fill_responses_in_text(txt_content, responses)
save_conversation_to_file(output_text, 'input_conversation.txt')
