from flask import request
from pymessenger import Bot

from sharesio import app
from sharesio.config import config
from sharesio.event_dispatcher import EventDispatcher
from sharesio.face_recognition import FaceRecognition
from sharesio.messenger_api import MessengerApi
from sharesio.messenger_bot import MessengerBot
from sharesio.repository import InMemoryImageRepository, InMemoryUserRepository

_pymessenger_bot = Bot(config['page_access_token'])

_api = MessengerApi(_pymessenger_bot)
_face_recognition = FaceRecognition()
_image_repository = InMemoryImageRepository()
_user_repository = InMemoryUserRepository()
_messenger_bot = MessengerBot(_api, _face_recognition, _image_repository, _user_repository)

_event_dispatcher = EventDispatcher(_messenger_bot)


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
            if x.get('postback'):
                sender_id = x['sender']['id']
                if x['postback'].get('payload'):
                    payload = x['postback']['payload']
                    _event_dispatcher.on_postback(sender_id, payload)
            if x.get('message'):
                sender_id = x['sender']['id']
                if x['message'].get('text'):
                    text = x['message']['text']
                    _event_dispatcher.on_text_message(sender_id, text)
                if x['message'].get('attachments'):
                    for a in x['message']['attachments']:
                        _event_dispatcher.on_attachment(sender_id, a)
                if x['message'].get('quick_reply'):
                    if x['message']['quick_reply'].get('payload'):
                        _event_dispatcher.on_postback(sender_id, x['message']['quick_reply']['payload'])
    return 'ok'
