import abc


class ImageRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user_id, image_url):
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

    def save(self, user_id, image_url):
        if user_id not in self._images.keys():
            self._images[user_id] = set()
        self._images[user_id].add(image_url)

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
    def find_by_page_scoped_id(self, id):
        pass

    @abc.abstractmethod
    def delete_by_page_scoped_id(self, id):
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = []

    def save(self, user):
        if not self.find_by_page_scoped_id(user.page_scoped_id):
            self._users.append(user)

    def find_by_page_scoped_id(self, id):
        users = [u for u in self._users if u.page_scoped_id == id]
        if len(users) > 0:
            return users[0]
        else:
            return None

    def delete_by_page_scoped_id(self, id):
        self._users = [u for u in self._users if u.page_scoped_id != id]


class User:
    def __init__(self, page_scoped_id, first_name, last_name):
        self.page_scoped_id = page_scoped_id
        self.first_name = first_name
        self.last_name = last_name
        self._registered = False
        self.face_picture_url = None

    def register(self, face_picture_url):
        self._registered = True
        self.face_picture_url = face_picture_url

    def is_registered(self):
        return self._registered
