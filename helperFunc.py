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