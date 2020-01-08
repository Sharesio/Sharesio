import abc
from queue import SimpleQueue


class ImageRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user_id, embedding):
        pass

    @abc.abstractmethod
    def find_all(self):
        pass

    @abc.abstractmethod
    def find_all_by_user_id(self, user_id):
        pass

    @abc.abstractmethod
    def delete_all_by_user_id(self, user_id):
        pass


class InMemoryImageRepository(ImageRepository):
    def __init__(self):
        self._images = {}

    def save(self, user_id, embedding):
        if user_id not in self._images.keys():
            self._images[user_id] = []
        self._images[user_id] += [embedding]

    def find_all(self):
        return self._images

    def find_all_by_user_id(self, user_id):
        if user_id in self._images.keys():
            return self._images[user_id]
        else:
            return []

    def delete_all_by_user_id(self, user_id):
        self._images.pop(user_id, None)


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user):
        pass

    @abc.abstractmethod
    def find_by_id(self, id):
        pass

    @abc.abstractmethod
    def find_all_registered(self):
        pass

    @abc.abstractmethod
    def delete_by_id(self, id):
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}

    def save(self, user):
        if user.id not in self._users.keys():
            self._users[user.id] = user

    def find_by_id(self, id):
        if id in self._users.keys():
            return self._users[id]
        else:
            return None

    def find_all_registered(self):
        return {k: v for k, v in self._users.items() if v.is_registered}

    def delete_by_id(self, id):
        self._users.pop(id, None)


class User:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_registered = False
        self.embedding = None
        self._picture_with_faces = PictureWithFaces('', [])

    def register(self, embedding):
        self.is_registered = True
        self.embedding = embedding

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def add_unresolved_picture(self, picture_url, embeddings):
        if len(embeddings) > 0:
            self._picture_with_faces = PictureWithFaces(picture_url, embeddings)

    def has_unresolved_picture(self):
        return self._picture_with_faces.is_unresolved()

    def pop_next_unresolved_face(self):
        if self._picture_with_faces.is_unresolved():
            return self._picture_with_faces.pop_next_face()
        else:
            return None


class PictureWithFaces:
    def __init__(self, picture_url, embeddings):
        self._picture_url = picture_url
        self._embeddings = SimpleQueue()
        [self._embeddings.put(e) for e in embeddings]

    def pop_next_face(self):
        return self._picture_url, self._embeddings.get()

    def is_unresolved(self):
        return not self._embeddings.empty()
