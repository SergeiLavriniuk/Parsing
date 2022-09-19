# Parsing

main.py
Parser for shoes Marko company
def get_html requests information from the site about accsess and returns code of it
def get_content requests html code and sort parametres to cards from first pagee of site
def parser_data sort information from next pages of site and put it to results.json file

bot.py
recives code from main.py and send it to bot in Telegram
