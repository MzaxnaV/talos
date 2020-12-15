from datetime import timedelta, timezone
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

START_MSG = ('*How do i solve the captcha?*\nYou will be shown '
             'one or more rule(s) from our group rules. You must '
             'pick the correct ordinal number of the rule.\n\n'
             '*How many questions do i have to answer to be unmuted?*\n'
             'You must answer all 3 questions correctly.\n\n'
             '*How many attempts do i have?*\n'
             'You have 3 attempts. If you get 3 answers wrong, you will '
             'be kicked\n\n'
             '*Click start to begin the captcha*')

# Read the datetime.timezone documentation
tz = timezone(timedelta(hours=5, minutes=30))
# Ban period for users that failed captcha (in minutes)
# If set to 0 it will be a perma ban until manually unbanned
BAN_PERIOD = int(os.getenv('BAN_PERIOD'))
