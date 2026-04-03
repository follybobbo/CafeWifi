import time
from flask import session

# calculates the time
def check_if_session_key_is_expired(key: str):
    time_now = time.time()

    #note in the event that the key does not exist, expiry_time = 0 and hence, elapsed will be equals  +ve
    #hence meaning we might have to delete a key that does not exist.
    #we wll use a try except block to handle that in the login route

    expiry_time = session.get(key, 0)
    elapsed = time_now - expiry_time

    if elapsed >=0:
        return True

    return False


def set_key_in_session(key, value):
    session[key] = value

    #logging needed. ???

