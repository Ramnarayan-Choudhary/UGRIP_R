# Teacher and Student Interactions Util code and workflow

import os
from openai import AzureOpenAI
import datetime
import json

class Conversation:
    def __init__(self, client, model_name, role):
        self.role = role
        self.client = client
        self.model_name = model_name
        self.resp_dict = {}
        self.msg_text = []
        self.prev_resp = ""
        self.idx = 0

    def process_prompt(self, prompt, max_tokens=300):
        self.msg_text.append({"role": "system", "content": self.prev_resp})
        self.msg_text.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.msg_text,
            temperature=0,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        resp_content = completion.to_dict()['choices'][0]['message']['content']
        self.resp_dict[f'Prompt {self.idx + 1}'] = resp_content
        self.prev_resp = resp_content
        self.idx += 1

        # print(f"SUCCESS: prompt {self.idx} is processed.")

    def __str__(self):
        return f"{self.role} Answer {self.idx}: {self.prev_resp}"

def load_model(model_name):
    print(f"Loading {model_name}...")
    client = AzureOpenAI(
        azure_endpoint="https://cullmsouthindia.openai.azure.com/",
        api_key="037155e1b16a432fa836637370eca0e3",
        api_version="2024-02-15-preview"
    )
    print("SUCCESS: model loaded.")
    return client

def main():
    model_name = 'gpt4'
    teacher_convo = Conversation(load_model(model_name), model_name, 'Teacher')
    student_convo = Conversation(load_model(model_name), model_name, 'Student')

    prompt = 'Hello there, can you ask one funny question as a joke? Only state one question itself, nothing else.'
    print('Programmed Prompt 1: ' + prompt)
    # Ask question 1 to client 1
    teacher_convo.process_prompt(prompt, 100)
    print(teacher_convo)

    print('CLIENT 1 DONE WITH ITERATION {}\n'.format(teacher_convo.idx))

    # Pass along client 1's answer to client 2
    ans_prompt01 = 'Hi, can you answer this question: ' + teacher_convo.resp_dict[f'Prompt {teacher_convo.idx}'] + ' Only list the answer in one sentence. No explanations needed.'
    print('Question 01 for student: ' + ans_prompt01)
    student_convo.process_prompt(ans_prompt01)
    print(student_convo)

    # Ask question 2 to client 1
    ans_prompt02 = "Is this pun explained correctly? \n" + student_convo.resp_dict[f'Prompt {student_convo.idx}'] + ' Just say "yes" or "no".'
    print('Evaluation for teacher: ' + ans_prompt02)
    teacher_convo.process_prompt(ans_prompt02)
    print(teacher_convo)

    # Ask client 2 to modify the question, then send to client 1
    ans_prompt03 = "Can you come up with another question about camels? Just ask the question in one sentence, nothing else."
    print('Question 02 (camel) for teacher: ' + ans_prompt03)
    teacher_convo.process_prompt(ans_prompt03)
    print(teacher_convo)

    # Ask client 2 to modify the question, then send to client 1
    ans_prompt06 = "Can you answer this question in one sentence? " + teacher_convo.resp_dict[f'Prompt {teacher_convo.idx}']
    print('Question camel for student: ' + ans_prompt06)
    student_convo.process_prompt(ans_prompt06)
    print(student_convo)

    # Ask question 2 to client 1
    ans_prompt04 = "Is this statement correct? " + student_convo.resp_dict[f'Prompt {student_convo.idx}'] + " Just say 'yes' or 'no'."
    print('Evaluation 02 (camel) for teacher: ' + ans_prompt04)
    teacher_convo.process_prompt(ans_prompt04)
    print(teacher_convo)

    # Tell client 1 to do recall
    ans_prompt05 = "Looking through the message history, what are the topics we discussed in this conversation?"
    print("Teacher convo summary: " + ans_prompt05)
    teacher_convo.process_prompt(ans_prompt05)
    print(teacher_convo)

    print("Student convo summary: " + ans_prompt05)
    student_convo.process_prompt(ans_prompt05)
    print(student_convo)

    print('ALL INTERACTIONS FINISHED.')

if __name__ == "__main__":
    main()
