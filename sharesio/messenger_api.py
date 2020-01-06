import requests
from pymessenger import Bot

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
        return self._bot.send_raw(payload)

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
