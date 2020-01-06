from enum import Enum


class Postback(str, Enum):
    DELETE_ACCOUNT = 'POSTBACK_DELETE_ACCOUNT'
    CREATE_ACCOUNT = 'POSTBACK_CREATE_ACCOUNT'
    REGISTER_WITH_PROFILE_PICTURE = 'POSTBACK_REGISTER_WITH_PROFILE_PICTURE'
    REGISTER_WITH_UPLOADED_PICTURE = 'POSTBACK_REGISTER_WITH_UPLOADED_PICTURE'
