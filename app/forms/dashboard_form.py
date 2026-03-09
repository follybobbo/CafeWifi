from flask_wtf import FlaskForm
from wtforms import FileField, StringField

from wtforms.validators import DataRequired






class DashboardForm(FlaskForm):
    photo = FileField("Photo", validators=[])
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])