from sharesio.log import log
from sharesio.messenger_bot import MessengerBot
from sharesio.postback import Postback


class EventDispatcher:
    def __init__(self, bot: MessengerBot):
        self._bot = bot

    def on_postback(self, sender_id, payload):
        log(f"[{sender_id}] - received postback with payload: {payload}")

        if payload == Postback.DELETE_ACCOUNT:
            self._bot.delete_account(sender_id)

        elif payload == Postback.CREATE_ACCOUNT:
            self._bot.create_account(sender_id)

        elif payload == Postback.REGISTER_WITH_PROFILE_PICTURE:
            self._bot.register_with_profile_picture(sender_id)

        elif payload == Postback.REGISTER_WITH_UPLOADED_PICTURE:
            self._bot.register_with_uploaded_picture(sender_id)

    def on_text_message(self, sender_id, text_message):
        log(f"[{sender_id}] - received text message: {text_message}")

    def on_attachment(self, sender_id, attachment):
        log(f"[{sender_id}] - received attachment: {attachment}")
        if attachment['type'] == 'image':
            self._on_image_attachment(sender_id, attachment)
        else:
            log(f"[{sender_id}] - received unsupported attachment with type: {attachment['type']}")

    def _on_image_attachment(self, sender_id, image_attachment):
        # TODO: verify if this url is permanent (it is generated by Facebook so it might just be a temporary url)
        picture_url = image_attachment['payload']['url']
        if self._bot.is_user_registered(sender_id):
            self._bot.upload_picture(sender_id, picture_url)
        else:
            self._bot.upload_picture_for_registration(sender_id, picture_url)