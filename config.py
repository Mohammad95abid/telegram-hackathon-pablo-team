
import pymysql
import requests

API_KEYS = {
    "key": "q5QJR1BpwdBHs7SLjH0mw",
    "secret": "AVn3klr2VsZk5l8e4ia9hf55lTez5BSIankd7G9a94"
}


# NGROK = 'https://0f9b99641393.ngrok.io/message'
NGROK = 'https://6b4534d8ede5.ngrok.io/message'
# TOKEN = '1447831093:AAH1c0VxTtok89zxlMuxQR9oPvCmiriZq_4'
TOKEN = '1418798786:AAHZKbNqK1G2tokOT_aIfhuNuQW1ZCRsaGU'

TELEGRAM_HOST = 'https://api.telegram.org/bot'
SET_WEBHOOK = '/setWebhook?url='

URL = TELEGRAM_HOST + TOKEN + SET_WEBHOOK + NGROK


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="paplo",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if __name__ == '__main__':
    requests.get(URL)
