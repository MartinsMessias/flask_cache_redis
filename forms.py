from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class FiboForm(FlaskForm):
    number = IntegerField('Enter a non-negative integer',
                          validators=[InputRequired(), NumberRange(min=1, max=10000)])
    submit = SubmitField('Calculate')
