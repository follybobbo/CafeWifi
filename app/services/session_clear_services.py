from flask import session



def remove_certain_keys_session(session_key_list: list):
    for key in session_key_list:
        session.pop(key, None)


def remove_singular_key_from_session(key: str):
    session.pop(key, None)
    #log it somewhere later