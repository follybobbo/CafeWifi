from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VenueInfo(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])

    next = SubmitField("NEXT")