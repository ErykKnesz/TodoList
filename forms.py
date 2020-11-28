from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField


class TodoForm(FlaskForm):
    title = StringField('title')
    description = TextAreaField('description')
    done = BooleanField('done')