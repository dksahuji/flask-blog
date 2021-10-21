from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class CommentForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    content = TextAreaField("Content", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Comment')
