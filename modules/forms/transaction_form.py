# modules/forms/transaction_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    date = DateField(
        'Date',
        format='%Y-%m-%d',
        validators=[DataRequired(message="Please enter a valid date. Format: YYYY-MM-DD")]
    )
    amount = FloatField('Amount', validators=[DataRequired(message="Please enter a valid amount.")])
    description = StringField('Description', validators=[DataRequired(message="Description is required.")])
    debit_account = SelectField('Debit Account', coerce=int, validators=[DataRequired(message="Please select a debit account.")])
    credit_account = SelectField('Credit Account', coerce=int, validators=[DataRequired(message="Please select a credit account.")])
    submit = SubmitField('Create Transaction')
