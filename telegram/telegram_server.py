from flask import Flask, request, Response
import requests
import config
from telegram.bot import Bot

app = Flask(__name__)

@app.route('/sanity')
def sanity():return "server running"

@app.route('/message', methods=["POST"])
def handle_message():
    bot = Bot(request)
    bot.function_handler()
    # print("got message")
    # chat_id = request.get_json()['message']['chat']['id']
    # res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    #                    .format(config.TOKEN, chat_id, chat_id))
    return Response("success")





if __name__ == '__main__':
    requests.get(config.URL)
    app.run(port=5002)

