from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField

from wtforms.validators import DataRequired, Email, Length, EqualTo




class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password (8 characters minimum)", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long")])

    password_confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Passwords do not match")])

    register = SubmitField("REGISTER")