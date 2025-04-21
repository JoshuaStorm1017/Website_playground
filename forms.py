from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class QuoteForm(FlaskForm):
    """Form for requesting a quote."""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    company = StringField('Company', validators=[Length(max=100)])
    service_interested_in = StringField('Service Interested In', validators=[Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Request Quote')