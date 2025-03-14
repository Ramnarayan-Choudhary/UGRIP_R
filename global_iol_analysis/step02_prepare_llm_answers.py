# Format raw LLM answers into a evaluation json.
# Double check again that the format matches with that of "test.josn"

# out_json_name = os.path.join(out_path, source_lang, f"{source_lang}_{target_lang}_answers.json")
       

import json
import os

# Step00: Uesr config
list_of_source_langs = ['madak', 'dyirbal', 'wambaya', 'yonggom', 'kabardian', 'benabena']
# list_of_source_langs = ['kabardian', 'benabena']
list_of_target_langs = ['english', 'dutch', 'estonian']

# list_of_source_langs = ['dyirbal']
# list_of_target_langs = ['dutch']


# Config, don't change
raw_answers_path = 'output_json'
test_template_path = 'multiling_problem_set'
ref_path = 'multiling_ref'
out_path = 'multiling_llm_answers'

os.makedirs(out_path, exist_ok=True)

# Step01: Let GPT do the multilingual problems
for source_lang in list_of_source_langs: # madak
    for target_lang in list_of_target_langs: # english

        os.makedirs(os.path.dirname(os.path.join(out_path, source_lang)), exist_ok=True)

        # Load field 2 of the json
        answer_file = os.path.join(raw_answers_path, f"{source_lang}_{target_lang}_GPT_convo.json")
        with open(answer_file, 'r', encoding='utf-8') as file:
            answer_data = json.load(file)
        
    
        answer_data = json.loads(answer_data['Prompt 2'])

        # Grab its template test
        test_template = os.path.join(test_template_path, 
            source_lang, f"{source_lang}_{target_lang}_test.json")
        with open(test_template, 'r', encoding='utf-8') as file:
            test_data = json.load(file)

        new_ans_list = []
        test_data_copy = test_data

        for ans, test in zip(answer_data['test'], test_data['test']):
            new_ans = ans.copy()  # Make a copy of the ans
            third_element = test[2]  # Get the third element of the test data
            
            # Check if the answers are out of order, then fix it
            if ans[0] == test[1]:
                new_ans[0] = ans[1]
                new_ans[1] = ans[0]
            # Check if the third element is ">" or "<"
            if third_element == '<':
                new_ans[1] = test[1]  # Populate the second element with the second element of the test data
            elif third_element == '>':
                new_ans[0] = test[0]  # Populate the first element with the second element of the test data
        
            new_ans[2] = test[2]
            new_ans_list.append(new_ans)

            print(ans)
            print(test)
            print(new_ans)
            print("\n")
        
        

        # Append any remaining elements from test_data['test']
        if len(test_data['test']) > len(answer_data['test']):
            for remaining_test in test_data['test'][len(answer_data['test']):]:
                new_ans_list.append(remaining_test)

        test_data_copy['test'] = new_ans_list
        new_json_string = json.dumps(test_data_copy, indent=2, separators=(',', ':'), ensure_ascii=False)

        out_json_name = os.path.join(out_path, source_lang, f"{source_lang}_{target_lang}_answers.json")
        os.makedirs(os.path.dirname(out_json_name), exist_ok=True)
        with open(out_json_name, 'w', encoding='utf-8') as file:
            file.write(new_json_string) 

        print(f"SUCCESS: {out_json_name} saved.")
     