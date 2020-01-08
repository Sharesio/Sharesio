import json

import requests
from PIL import Image
from pymessenger import Bot
from requests_toolbelt import MultipartEncoder

from sharesio.config import config


class MessengerApi:
    def __init__(self, bot: Bot):
        self._bot = bot

    def url(self):
        return self._bot.graph_url

    def send_text_message(self, recipient_id, message):
        self._bot.send_text_message(recipient_id, message)

    def send_quick_reply(self, recipient_id, message, quick_replies):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'messaging_type': 'RESPONSE',
            'message': {
                'text': message,
                'quick_replies': [q.to_text_payload() for q in quick_replies]
            }
        }
        self._bot.send_raw(payload)

    def send_picture(self, recipient_id, picture):
        Image.fromarray(picture).save('temp.png')
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'image',
                        'payload': {}
                    }
                }
            ),
            'filedata': ('temp.png', open('temp.png', 'rb'), 'image/png')
        }
        multipart_data = MultipartEncoder(payload)
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        return requests.post(
            f"{self._bot.graph_url}/me/messages",
            params=self._bot.auth_args,
            headers=multipart_header,
            data=multipart_data
        )

    def send_picture_url(self, recipient_id, picture_url):
        self._bot.send_image_url(recipient_id, picture_url)

    def get_person_details(self, id):
        endpoint = f"{self._bot.graph_url}/{id}?fields=first_name,last_name,profile_pic&access_token={config['page_access_token']}"
        return requests.get(endpoint).json()

    def get_person_profile_url(self, id):
        endpoint = f"{self._bot.graph_url}/{id}?fields=profile_pic&access_token={config['page_access_token']}"
        return requests.get(endpoint).json()['profile_pic']

    def get_person_first_and_last_name(self, id):
        endpoint = f"{self._bot.graph_url}/{id}?fields=first_name,last_name&access_token={config['page_access_token']}"
        person_details = requests.get(endpoint).json()
        return person_details['first_name'], person_details['last_name']

    def get_person_full_name(self, id):
        endpoint = f"{self._bot.graph_url}/{id}?fields=first_name,last_name&access_token={config['page_access_token']}"
        person_details = requests.get(endpoint).json()
        return f"{person_details['first_name']} {person_details['last_name']}"
