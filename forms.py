from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, DateField, StringField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        'Password', [InputRequired(), Length(4, 20),
                     EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Register")


class AddBook(FlaskForm):
    book = StringField("Book", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    submit = SubmitField("Add book")


class AddPages(FlaskForm):
    page = StringField("Page", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    submit = SubmitField("Add pages")
