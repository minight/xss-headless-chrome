from flask_wtf import Form
from wtforms import TextField, SubmitField, TextAreaField, PasswordField

class loginform(Form):
    username = TextField("username")
    password = PasswordField("password")
    submit = SubmitField("go!")
