from app.models import User
from app.extensions import db



def get_user(user_id: int):
    user = db.get_or_404(User, user_id)

    return user



def get_user_by_email(email: str):
    user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

    return user


def create_new_user(email, name, surname, city, hashed_password):

    new_user = User(
        email=email,
        name=name,
        surname=surname,
        city=city,
        hashed_password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return new_user

def create_user_data_for_dashboard(the_current_user):
    user_data = {
        "first_name": the_current_user.name,
        "surname": the_current_user.surname,
        "email": the_current_user.email,
        "picture_url": the_current_user.profile_picture_url
    }

    return user_data


def update_user_email_verification_status(the_user, update_status: bool):
    the_user.verified = update_status
    db.session.commit()


def update_user_display_picture(user_id: int, picture_path: str):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar_one_or_none()
    if user:
        user.profile_picture = picture_path
        db.session.commit()


