from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired


my_choices = [('life', 'Life'),  ('inspiration', 'Inspiration'), ('philosophy', 'Philosophy'), ('ml', 'Machine Learning'), ('personalfinance', 'Personal Finance'), ('quotes', 'Quotes'), ('technology', 'Technology')]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    abstract = TextAreaField("Abstract", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    type_select = RadioField("Type_select", choices=[('text','text'),('markdown','markdown')], validators=[DataRequired()])
    tags = SelectMultipleField("Tags", choices = my_choices, default=[])    
    text_tags = StringField("Text_tags")
    submit = SubmitField("Post")

