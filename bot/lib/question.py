from telegram import InlineKeyboardButton,  InlineKeyboardMarkup
from .common import rules
import random


class Question:
    def __init__(self,  group_id, total_iterations):
        self.iteration = 0
        self.total_iterations = total_iterations
        self.questions = []
        self.answers = []
        self.choices = []

        for i in range(total_iterations):
            self.generate_question()

    def __add__(self, num):
        self.iteration = self.iteration + num

    def __eq__(self, val):
        return (val == self.answers[self.iteration])

    def generate_question(self):
        question = random.choice(range(0, len(rules)))
        answer = question + 1
        choices = [answer]

        # Ensure its unique
        if answer in self.answers:
            return self.generate_question(self)

        while len(choices) < 4:
            rand_choice = random.choice(range(1, len(rules)+1))
            if(rand_choice != question and rand_choice not in choices):
                choices.append(rand_choice)

        random.shuffle(choices)
        self.questions.append(rules[question])
        self.answers.append(answer)
        self.choices.append(choices)
        print(self.questions)
        print(self.answers)

    def __str__(self):
        return (f'Question {self.iteration+1}/{self.total_iterations}\n'
                f'{self.questions[self.iteration]}\n')

    def answer_choices(self):
        callback = 'verify_captcha_{group_id}'
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text=choice,
                                     callback_data=f'{callback}_{choice}')
            ]
            for choice in self.choices[self.iteration]
        ])

    def __get_state__(self):
        return self.__dict__

    def __set_state__(self, data):
        self.__dict__ = self.data
