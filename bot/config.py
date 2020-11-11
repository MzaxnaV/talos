from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
RULES_URI = os.getenv('RULES_URI')
RULES_URI_HUMAN = os.getenv('RULES_URI_HUMAN')
ENABLE_WELCOME_MSG = bool(os.getenv('ENABLE_WELCOME_MSG'))

WELCOME_MSG = ('Hello {username}, welcome to the group. You have been muted.'
               '\nPlease follow the instructions to unmute yourself.')

START_MSG = ('Hello there,\nYou have been muted.\nTo ensure smooth interaction'
             ' in this community, you are required to read the rules and solve'
             ' this captcha in order to verify that you have done the  same.\n'
             'At which number is the following rule listed in @pyindiarules\n'
             '\n*{question}*')
