from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class SearchVenue(FlaskForm):
    location = StringField("SEARCH THE VENUE", validators=[DataRequired()])
    location_url = StringField("LOCATION URL", validators=[DataRequired()])
    photo = StringField("choose a photo", validators=[DataRequired()])
    city = StringField("CITY", validators=[DataRequired()])
    country = StringField("COUNTRY", validators=[DataRequired()])
    street_one = StringField("Street", validators=[DataRequired()])


    next = SubmitField("NEXT")


class VenueInfo(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])

    next = SubmitField("NEXT")