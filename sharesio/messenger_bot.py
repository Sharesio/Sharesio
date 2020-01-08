import imageio

from sharesio.face_recognition import FaceRecognition
from sharesio.messenger_api import MessengerApi
from sharesio.quick_reply import QuickReplies
from sharesio.repository import User, ImageRepository, UserRepository


class MessengerBot:
    def __init__(self, api: MessengerApi, face_recognition: FaceRecognition, image_repository: ImageRepository, user_repository: UserRepository):
        self._api = api
        self._face_recognition = face_recognition
        self._image_repository = image_repository
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

    # TODO: the same person can't be more than 1 time on a single picture
    # TODO: maybe use some threshold (if more than 90% sure than don't ask, otherwise ask)
    def upload_picture(self, user_id, picture_url):
        faces_dict = self._image_repository.find_all()
        picture = imageio.imread(picture_url)
        embeddings = self._face_recognition.face_embeddings(picture)
        matching_user_ids = set()
        unrecognised_faces = set()
        for i, embedding in enumerate(embeddings):
            matching_user_id = self._face_recognition.find_matching_user_id(embedding, faces_dict)
            if matching_user_id:
                matching_user_ids.add(matching_user_id)
                self._image_repository.save(matching_user_id, embedding)
            else:
                unrecognised_faces.add(i)

        for id in matching_user_ids:
            if id != user_id:
                self._api.send_text_message(id, f"{self._api.get_person_full_name(user_id)} uploaded a picture with you:")
                self._api.send_picture_url(id, picture_url)

        registered_users = self._user_repository.find_all_registered()
        matching_names = [registered_users[id].full_name() for id in matching_user_ids if id != user_id]
        if len(matching_names) > 0:
            self._api.send_text_message(user_id, f"Picture was sent to: {', '.join(matching_names)}.")

        if len(unrecognised_faces) > 0:
            self._user_repository.find_by_id(user_id).add_unresolved_picture(picture_url, [e for i, e in enumerate(embeddings) if i in unrecognised_faces])
            faces = self._face_recognition.get_cropped_faces_from_image(picture)
            self._api.send_text_message(user_id, f"Couldn't recognise {len(unrecognised_faces)} out of {len(embeddings)} faces. Please input their names in the following order:")
            for i in unrecognised_faces:
                self._api.send_picture(user_id, faces[i])

    def resolve_next_face(self, user_id, suggested_full_name):
        picture_url, embedding = self._user_repository.find_by_id(user_id).pop_next_unresolved_face()
        matching_users = [user for id, user in self._user_repository.find_all_registered().items() if user.full_name() == suggested_full_name]
        if len(matching_users) > 0:
            matched_user = matching_users[0]
            self._image_repository.save(matched_user.id, embedding)
            self._api.send_text_message(matched_user.id, f"{self._api.get_person_full_name(user_id)} uploaded a picture with you:")
            self._api.send_picture_url(matched_user.id, picture_url)
            self._api.send_text_message(user_id, f"Picture was sent to {matched_user.full_name()}.")
        else:
            self._api.send_text_message(user_id, f"{suggested_full_name} is not registered.")

    def is_user_registered(self, user_id):
        user = self._user_repository.find_by_id(user_id)
        if user is not None:
            return user.is_registered
        else:
            return False

    def is_user_resolving_faces(self, user_id):
        return self._user_repository.find_by_id(user_id).has_unresolved_picture()
