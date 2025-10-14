from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class SearchVenue(FlaskForm):
    location = StringField("name", validators=[DataRequired()])
    location_url = StringField("location_url", validators=[DataRequired(), URL()])
    photo = StringField("photo_url", validators=[DataRequired(), URL()])


    next = SubmitField("next")


class VenueInfo(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    street = StringField("street", validators=[DataRequired()])