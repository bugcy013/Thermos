__author__ = 'dhana013'

from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired, url
from wtforms.fields.html5 import URLField

class BookmarkForm(Form):
    url = URLField('url', validators=[DataRequired(), url()])
    description = StringField('description')


