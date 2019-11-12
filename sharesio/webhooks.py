from flask import request

from sharesio import app
from sharesio.config import config
from sharesio.messenger_bot import MessengerBot

_bot = MessengerBot()


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/webhook', methods=['GET'])
def verify_token():
    if request.args.get('hub.verify_token') == config['verification_token']:
        return request.args.get('hub.challenge')
    else:
        return 'Invalid verification token'


@app.route('/webhook', methods=['POST'])
def on_message():
    for event in request.json['entry']:
        for x in event['messaging']:
            if x.get('message'):
                sender_id = x['sender']['id']
                if x['message'].get('text'):
                    text = x['message']['text']
                    _bot.on_text_message(sender_id, text)
                if x['message'].get('attachments'):
                    for a in x['message']['attachments']:
                        _bot.on_attachment(sender_id, a)
    return 'ok'
