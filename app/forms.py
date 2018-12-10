from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    address = StringField('FLO address', validators=[DataRequired()])
    submit = SubmitField('Search')

class BlankForm(FlaskForm):
    pass

