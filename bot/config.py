from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
BOT_MASTER = int(os.getenv('BOT_MASTER'))
RULES_URI = os.getenv('RULES_URI')
RULES_URI_HUMAN = os.getenv('RULES_URI_HUMAN')
ENABLE_WELCOME_MSG = bool(int(os.getenv('ENABLE_WELCOME_MSG')))

QUESTION_QUANTITY = int(os.getenv('QUESTION_QUANTITY'))
ERRORS_ALLOWED = int(os.getenv('ERRORS_ALLOWED'))

WELCOME_MSG = ('Hello {username}, welcome to the group. You have been muted.'
               '\nPlease follow the instructions to unmute yourself.')

START_MSG = ('Hello there,\nYou have been muted.\nTo ensure smooth interaction'
             ' in this community, you are required to read the rules and solve'
             ' this captcha in order to verify that you have done the  same.\n'
             'At which number is the following rule listed in @pyindiarules\n'
             '\n*{question}*')
