# This file contains all the helper functions needed in backend
######################
from flask_hashing import Hashing


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
