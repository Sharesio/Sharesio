from sharesio.postback import Postback


class QuickReply:
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
    def profile_picture():
        return [
            QuickReply('Use profile picture', None, Postback.REGISTER_WITH_PROFILE_PICTURE),
            QuickReply('Upload new picture', None, Postback.REGISTER_WITH_UPLOADED_PICTURE)
        ]
