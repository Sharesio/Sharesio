import face_recognition


class FaceRecognition:

    @staticmethod
    def extract_face_encoding(image):
        """
        Parameters
        ----------
        image: numpy array (image should only contain one face)
        Returns
        -------
        Face embedding of the input image if face embedding could be calculated.
        None if no face or more than one face was found.
        """
        embedding = face_recognition.face_encodings(image)
        if len(embedding) == 1:
            return embedding[0]
        elif len(embedding) == 0:
            return None
        elif len(embedding) > 1:
            return None

    @staticmethod
    def face_embeddings(image):
        """
        Returns a list of all face embeddings found in the input image.
        """
        return face_recognition.face_encodings(image)

    @staticmethod
    def face_locations(image):
        return face_recognition.face_locations(image)

    @staticmethod
    def get_cropped_faces_from_image(image):
        """
        Finds all faces in an image.
        Returns
        -------
        List of faces images as numpy arrays.
        """
        face_locations = face_recognition.face_locations(image)
        face_list = []
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            face_list.append(face_image)
        return face_list

    @staticmethod
    def compare_embeddings(known_face_embeddings, face_embedding_to_check):
        """
        Compare a list of face embeddings against a candidate embedding to see if they match.
        :param known_face_embeddings: A list of known face embeddings
        :param face_embedding_to_check: A single face embedding to compare against the list
        Returns
        -------
        A list of True/False values indicating which known_face_embeddings match the face embedding to check
        """
        return face_recognition.compare_faces(known_face_embeddings, face_embedding_to_check, tolerance=0.6)

    def find_matching_user_id(self, embedding_to_check, faces_dict):
        """
        Compares a face embedding with all face embeddings in the dictionary.
        :param embedding_to_check: embedding to check against the database as numpy array
        :param faces_dict: Dictionary in form {user_id: [embedding]}
        Returns
        -------
        If a match was found, the user_id with matching embedding will be returned.
        If no match was found, None will be returned.
        """
        for user_id, embeddings in faces_dict.items():
            if True in self.compare_embeddings(embeddings, embedding_to_check):
                return user_id
        return None
