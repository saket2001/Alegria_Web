# This file contains all the helper functions needed in backend
######################
from flask_hashing import Hashing
from decouple import config


hashing = Hashing()
######################

# To has any value


def hashValue(value):
    return hashing.hash_value(value, salt=config("HASH_KEY"))

# to check hash value against normal value


def compareHashValues(hashed_value, value):
    if hashing.check_value(hashed_value, value, salt='alegriahashkey'):
        return True
    else:
        return False


def generate_global_api_key():
    api_key = hashing.hash_value(config("SESSION_KEY"), salt="alegriahashkey")
    return api_key

# filter values
def filterList(arr):
    filteredArr=set(arr)
    return list(filteredArr)

# compare values across lists
def compareLists(list1,list2):
    list3=[]
    for x in list1:
        if x not in list2:
            list3.append(x)
    
    return list3
