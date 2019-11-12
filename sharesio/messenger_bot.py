from pymessenger.bot import Bot

from sharesio.config import config
from sharesio.log import log
from sharesio.repository import ImageInMemoryRepository


class MessengerBot:
    def __init__(self):
        self._bot = Bot(config['page_access_token'])
        self._image_repository = ImageInMemoryRepository()

    def on_text_message(self, sender_id, text_message):
        log(f"[{sender_id}] - received text message: {text_message}")
        if text_message.lower() == 'count':
            images = self._image_repository.get_images_by_user_id(sender_id)
            self._bot.send_text_message(recipient_id=sender_id, message=f"You sent {len(images)} unique pictures")

    def on_attachment(self, sender_id, attachment):
        log(f"[{sender_id}] - received attachment: {attachment}")
        if attachment['type'] == 'image':
            self._on_image_attachment(sender_id, attachment)
        else:
            response = f"Attachment of type [{attachment['type']}] is not supported"
            self._bot.send_text_message(recipient_id=sender_id, message=response)

    def _on_image_attachment(self, sender_id, image_attachment):
        global_user_id = self._local_to_global_user_id(sender_id)
        url = image_attachment['payload']['url']
        self._image_repository.save(global_user_id, url)
        self._bot.send_text_message(recipient_id=sender_id, message='Image was successfully submitted!')

    def _local_to_global_user_id(self, local_user_id):
        # TODO: convert local sender_id to global user-id and save it in db
        return local_user_id
