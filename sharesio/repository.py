class ImageInMemoryRepository:
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


class UserInMemoryRepository:
    def __init__(self):
        self._users = []

    def save(self, user):
        if not self.find_by_page_scoped_id(user.page_scoped_id):
            self._users.append(user)

    def find_by_page_scoped_id(self, id):
        return filter(lambda u: u.page_scoped_id == id, self._users)


class User:
    def __init__(self, page_scoped_id, first_name, last_name):
        self.page_scoped_id = page_scoped_id
        self.first_name = first_name
        self.last_name = last_name
