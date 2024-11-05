# modules/forms/account_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from modules.models.account import Account

class AccountForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired()])
    type = SelectField('Account Type', choices=[
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Equity', 'Equity'),
        ('Revenue', 'Revenue'),
        ('Expense', 'Expense')
    ], validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_name(self, field):
        if Account.query.filter_by(name=field.data).first():
            raise ValidationError('Account name already exists.')