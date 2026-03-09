from flask_login import current_user
from functools import wraps
from flask import redirect, url_for




def email_verification_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        is_verified = current_user.verified

        if not is_verified:
            return redirect(url_for("protected.unverified"))

        return f(*args, **kwargs)
    return wrapper