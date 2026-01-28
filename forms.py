from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField, EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class SearchVenue(FlaskForm):
    location = StringField("SEARCH THE VENUE", validators=[DataRequired()])
    location_url = StringField("LOCATION URL", validators=[DataRequired()])
    photo = StringField("choose a photo", validators=[DataRequired()])
    city = StringField("CITY", validators=[DataRequired()])
    country = StringField("COUNTRY", validators=[DataRequired()])
    street_one = StringField("Street", validators=[DataRequired()])
    latitude = DecimalField("latitude", validators=[DataRequired()])
    longitude = DecimalField("longitude", validators=[DataRequired()])


    next = SubmitField("NEXT")


class VenueInfo(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])

    next = SubmitField("NEXT")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired])

    login = SubmitField("LOG IN")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password (8 characters minimum)", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm password", validators=[DataRequired()])

    register = SubmitField("REGISTER")