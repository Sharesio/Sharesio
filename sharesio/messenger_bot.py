import imageio

from sharesio.face_recognition import FaceRecognition
from sharesio.messenger_api import MessengerApi
from sharesio.quick_reply import QuickReplies
from sharesio.repository import User, ImageRepository, UserRepository


class MessengerBot:
    def __init__(self, api: MessengerApi, face_recognition: FaceRecognition, image_repository: ImageRepository, user_repository: UserRepository):
        self._api = api
        self._face_recognition = face_recognition
        self._image_repository = image_repository  # TODO: image repository might be redundant
        self._user_repository = user_repository

    def create_account(self, user_id):
        if self._user_repository.find_by_id(user_id):
            self._api.send_text_message(user_id, 'You already have an account.')
        else:
            first_name, last_name = self._api.get_person_first_and_last_name(user_id)
            user = User(user_id, first_name, last_name)
            self._user_repository.save(user)
            self._api.send_quick_reply(user_id, 'Which picture of your face do you want to use?', QuickReplies.profile_picture())

    def delete_account(self, user_id):
        if self._user_repository.find_by_id(user_id):
            self._image_repository.delete_all_by_user_id(user_id)
            self._user_repository.delete_by_id(user_id)
            self._api.send_text_message(user_id, 'Thank you for using Sharesio!')
        else:
            self._api.send_text_message(user_id, "You don't have an account.")

    def help(self, user_id):
        self._api.send_text_message(user_id, 'For help please visit the documentation.')

    def register_with_profile_picture(self, user_id):
        picture_url = self._api.get_person_profile_url(user_id)
        self.register(user_id, picture_url)

    def register_with_uploaded_picture(self, user_id):
        self._api.send_text_message(user_id, 'Upload a picture of your face.')

    def register(self, user_id, picture_url):
        picture = imageio.imread(picture_url)
        embeddings = self._face_recognition.face_embeddings(picture)
        if len(embeddings) == 1:
            user = self._user_repository.find_by_id(user_id)
            user.register(embeddings[0])
            self._user_repository.save(user)
            self._image_repository.save(user_id, embeddings[0])
            self._api.send_text_message(user_id, f"Registration successful, welcome in Sharesio!")
        else:
            self._api.send_text_message(user_id, f"The picture should contain exactly 1 face, but it contains {len(embeddings)} faces. Please upload a new picture.")

    def upload_picture(self, user_id, picture_url):
        faces_dict = self._image_repository.find_all()
        picture = imageio.imread(picture_url)
        embeddings = self._face_recognition.face_embeddings(picture)
        matching_user_ids = []
        for i, embedding in enumerate(embeddings):
            matching_user_id = self._face_recognition.find_matching_user_id(embedding, faces_dict)
            if matching_user_id:
                matching_user_ids += [matching_user_id]
                self._image_repository.save(matching_user_id, embedding)
            else:
                pass  # TODO: face was not recognised

        for id in matching_user_ids:
            # if id != user_id:  # TODO: uncomment
            self._api.send_text_message(id, f"{self._api.get_person_full_name(user_id)} uploaded a picture with your face:")
            self._api.send_picture(id, picture_url)
            self._api.send_text_message(id, f"You now have {len(self._image_repository.find_all_by_user_id(user_id))} embeddings.")

        # TODO: if some faces are not recognized then ask the user to provide their names
        # TODO: the same person can't be more than 1 time on a single picture
        # TODO: ask the user if the match made by the system is correct (using quick replies)?
        # TODO: maybe use some threshold (if more than 90% sure than don't ask, otherwise ask)

        registered_users = self._user_repository.find_all_registered()
        matching_names = [registered_users[id].full_name() for id in matching_user_ids]  # TODO: remove sender name
        self._api.send_text_message(user_id, f"Picture was sent to: {', '.join(matching_names)}.")

    def is_user_registered(self, user_id):
        user = self._user_repository.find_by_id(user_id)
        if user is not None:
            return user.is_registered
        else:
            return False
