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
        picture = imageio.imread(picture_url)
        embedding = self._face_recognition.extract_face_encoding(picture)  # TODO: embedding can be None if no face or too many faces are found
        # self._image_repository.save(user_id, embedding)

        user = self._user_repository.find_by_id(user_id)
        user.register(embedding)
        self._user_repository.save(user)
        self._api.send_text_message(user_id, f"Your profile picture will be used as your face. Welcome in Sharesio!")

    def register_with_uploaded_picture(self, user_id):
        self._api.send_text_message(user_id, 'Upload a picture of your face.')

    def upload_picture_for_registration(self, user_id, picture_url):
        picture = imageio.imread(picture_url)
        embedding = self._face_recognition.extract_face_encoding(picture)  # TODO: embedding can be None if no face or too many faces are found
        # self._image_repository.save(user_id, embedding)

        user = self._user_repository.find_by_id(user_id)
        user.register(embedding)
        self._user_repository.save(user)
        self._api.send_text_message(user_id, f"The uploaded picture will be used as your face. Welcome in Sharesio!")

    def upload_picture(self, user_id, picture_url):
        registered_users = self._user_repository.find_all_registered()
        faces_dict = {k: v.embedding for k, v in registered_users.items()}
        picture = imageio.imread(picture_url)
        embeddings = self._face_recognition.get_encodings_from_image(picture)

        matching_user_ids = []
        for embedding in embeddings:
            matching_user_id = self._face_recognition.find_match(embedding, faces_dict)
            if matching_user_id is not None:
                matching_user_ids += [matching_user_id]
            else:
                pass  # TODO: face was not recognised

        matching_names = [f"{registered_users[id].first_name} {registered_users[id].last_name}" for id in matching_user_ids]
        self._api.send_text_message(user_id, f"Recognized: {', '.join(matching_names)}.")

        for id in matching_user_ids:
            if id != user_id:
                pass  # TODO: send the picture to user with this id

        # TODO: if some faces are not recognized then ask the user to provide their names
        # TODO: the same person can't be more than 1 time on a single picture
        # TODO: ask the user if the match made by the system is correct (using quick replies)?
        # TODO: maybe use some threshold (if more than 90% sure than don't ask, otherwise ask)
        # TODO: consider saving all face embeddings of every user so that a new face can be matched to all previous embeddings
        self._api.send_text_message(user_id, 'Picture was successfully submitted.')

    def is_user_registered(self, user_id):
        user = self._user_repository.find_by_id(user_id)
        if user is not None:
            return user.is_registered
        else:
            return False
