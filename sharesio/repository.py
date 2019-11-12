class ImageInMemoryRepository:
    def __init__(self):
        self._map = {}

    def save(self, user_id, image_url):
        if user_id not in self._map.keys():
            self._map[user_id] = set()
        self._map[user_id].add(image_url)

    def get_images_by_user_id(self, user_id):
        if user_id in self._map.keys():
            return self._map[user_id]
        else:
            return []
