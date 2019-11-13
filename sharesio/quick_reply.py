from enum import Enum


class QuickReply:
    class Postback(str, Enum):
        YES = 'QUICK_REPLY_POSTBACK_YES'
        NO = 'QUICK_REPLY_POSTBACK_NO'

    def __init__(self, title, image_url, postback_payload):
        self._title = title
        self._image_url = image_url
        self._postback_payload = postback_payload

    def to_text_payload(self):
        return {
            'content_type': 'text',
            'title': self._title,
            'image_url': self._image_url,
            'payload': self._postback_payload
        }


class QuickReplies:
    @staticmethod
    def yes_or_no():
        return [
            QuickReply('Yes', None, QuickReply.Postback.YES),
            QuickReply('No', None, QuickReply.Postback.NO)
        ]
