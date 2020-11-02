# Rules captcha bot

A simple telegram bot that will enforce a captcha based on your group rules to
newly joining members of your group  chat.

## Deploying
1) copy .env.example to .env
2) modify RULES_URI to point to a json file. This file is downloaded when the bot is initialized. For example
```
RULES_URI=https://raw.githubusercontent.com/1337neo/pythonindia/master/rules/languages/english/rules.json
```
3) Make sure to set 'BOT_USERNAME' in the .env file. It is used to check if
updates should be ignored or processed

### Other
1)  On paper this bot should seamlessly work across multiple groups, but with a single set of rules. 
	However this has not been tested.

2)  If you need to modify the message of the captcha question, you have to edit line 15-19 of **bot/lib/common.py**
```
qstn = ('Hello there,\nYou have been muted.\nTo ensure smooth interaction'
        ' in this community, you are required to read the rules and solve'
        ' this captcha in order to verify that you have done the  same.\n'
        'At which number is the following rule listed in @pyindiarules\n'
        '\n*{question}*')
```
