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

    def save(self, user_id, embedding):
        if user_id not in self._images.keys():
            self._images[user_id] = []
        self._images[user_id] += [embedding]

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

    def register(self, embedding):
        self.is_registered = True
        self.embedding = embedding
