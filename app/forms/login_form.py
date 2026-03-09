from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField

from wtforms.validators import DataRequired



class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("LOG IN")