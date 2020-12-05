from telegram import InlineKeyboardButton,  InlineKeyboardMarkup
from .common import rules
import random


class WrongAnswerError(Exception):
    pass


class Captcha:
    def __init__(self,  group_id, total_iterations, errors_allowed):
        self.group_id = group_id
        self.iteration = 0
        self.total_iterations = total_iterations
        self.errors_allowed = errors_allowed
        self.solved = 0
        self.wrong = 0
        self.questions = []
        self.answers = []
        self.choices = []

        for i in range(total_iterations):
            self.generate_question()

    # Sets captcha to the next question
    # and increments solved counter
    def __add__(self, num):
        self.iteration = self.iteration + num
        self.solved = self.solved + num

    # Increments wrong counter
    # Used to count how many wrong attempts were made
    def __sub__(self, num):
        self.wrong = self.wrong + num

    def __eq__(self, val):
        if int(val) == self.answers[self.iteration]:
            return True
        else:
            raise WrongAnswerError

    def has_failed(self):
        return (self.wrong >= self.errors_allowed)

    def is_solved(self):
        return (self.solved == self.total_iterations)

    def generate_question(self):
        question = random.choice(range(0, len(rules)))
        answer = question + 1
        choices = [answer]

        # Ensure its unique
        if answer in self.answers:
            return self.generate_question()

        while len(choices) < 4:
            rand_choice = random.choice(range(1, len(rules)+1))
            if(rand_choice != question and rand_choice not in choices):
                choices.append(rand_choice)

        random.shuffle(choices)
        self.questions.append(rules[question])
        self.answers.append(answer)
        self.choices.append(choices)

    def __str__(self):
        return (f'Question {self.iteration+1}/{self.total_iterations}\n'
                f'{self.questions[self.iteration]}\n')

    def answer_choices(self):
        callback = f'verify_captcha_{self.group_id}'
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
