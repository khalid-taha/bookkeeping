# modules/forms/transaction_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    debit_account = SelectField('Debit Account', coerce=int, validators=[DataRequired()])
    credit_account = SelectField('Credit Account', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Transaction')
