from sharesio.messenger_api import MessengerApi
from sharesio.quick_reply import QuickReplies
from sharesio.repository import User, ImageRepository, UserRepository


class MessengerBot:
    def __init__(self, api: MessengerApi, image_repository: ImageRepository, user_repository: UserRepository):
        self._api = api
        self._image_repository = image_repository
        self._user_repository = user_repository

    def delete_account(self, user_id):
        self._image_repository.delete_all_by_user_id(user_id)
        self._user_repository.delete_by_page_scoped_id(user_id)
        self._api.send_text_message(user_id, 'Thank you for using Sharesio!')

    def create_account(self, user_id):
        first_name, last_name = self._api.get_person_first_and_last_name(user_id)
        user = User(user_id, first_name, last_name)
        self._user_repository.save(user)
        self._api.send_quick_reply(user_id, 'Which picture of your face do you want to use?', QuickReplies.profile_picture())

    def register_with_profile_picture(self, user_id):
        picture_url = self._api.get_person_profile_url(user_id)
        self._image_repository.save(user_id, picture_url)
        user = self._user_repository.find_by_page_scoped_id(user_id)
        user.register(picture_url)
        self._user_repository.save(user)
        self._api.send_text_message(user_id, f"Your profile picture will be used as your face. Welcome in Sharesio!")

    def register_with_uploaded_picture(self, user_id):
        self._api.send_text_message(user_id, 'Upload a picture of your face.')

    def upload_picture_for_registration(self, user_id, picture_url):
        user = self._user_repository.find_by_page_scoped_id(user_id)
        user.register(picture_url)
        self._user_repository.save(user)
        self._api.send_text_message(user_id, f"The uploaded picture will be used as your face. Welcome in Sharesio!")

    def upload_picture(self, user_id, picture_url):
        self._image_repository.save(user_id, picture_url)
        # TODO: recognize faces on the picture
        # TODO: send the picture to recognized people
        # TODO: if some faces are not recognized then ask the user to provide their names
        self._api.send_text_message(user_id, 'Picture was successfully submitted.')

    def is_user_registered(self, user_id):
        user = self._user_repository.find_by_page_scoped_id(user_id)
        if user is not None:
            return user.is_registered()
        else:
            return False
