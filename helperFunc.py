# This file contains all the helper functions needed in backend
######################
from flask_hashing import Hashing
from decouple import config


hashing = Hashing()
######################

# To has any value


def hashValue(value):
    return hashing.hash_value(value, salt='alegriahashkey')

# to check hash value against normal value


def compareHashValues(hashed_value, value):
    if hashing.check_value(hashed_value, value, salt='alegriahashkey'):
        return True
    else:
        return False


def generate_global_api_key():
    api_key = hashing.hash_value(config("SESSION_KEY"), salt="alegriahashkey")
    return api_key