import face_recognition


class FaceRecognition:
    def __init__(self):
        pass

    @staticmethod
    def extract_face_encoding(image):
        """
        Parameters
        ----------
        image: numpy array (image should only contain one face)

        Returns
        -------
        Face encoding of the input image if face encoding could be calculated.
        None if no face or more than one face was found.
        """
        encoding = face_recognition.face_encodings(image)
        if len(encoding) == 1:
            return encoding
        elif len(encoding) == 0:
            return None
        elif len(encoding) > 1:
            return None

    @staticmethod
    def compare_face_encodings(known_face_encodings, face_encoding_to_check):
        """
        Compare a list of face encodings against a candidate encoding to see if they match.

        :param known_face_encodings: A list of known face encodings
        :param face_encoding_to_check: A single face encoding to compare against the list

        Returns
        -------
        A list of True/False values indicating which known_face_encodings match the face encoding to check
        """
        result = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)
        return result

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
    def get_encodings_from_image(image):
        """
        Returns a list of all face encodings found in the input image.
        """
        return face_recognition.face_encodings(image)

    def find_match_in_database(self, encoding_to_check, faces_dict):
        """
        Compares a face encoding with all face encodings in the database.
        :param encoding_to_check: Encoding to check against the database as numpy array
        :param faces_dict: Dictionary in form {"img_id"{"Name","Encoding"}}

        Returns
        -------
        If a match was found, the face encoding of the match will be returned.
        If no match was found, None will be returned.

        """
        for face_id, face_info in faces_dict.items():
            is_match = self.compare_face_encodings(face_info['Encoding'], encoding_to_check)[0]
            if is_match:
                return face_id, face_info
        return None



