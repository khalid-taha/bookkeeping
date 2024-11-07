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
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self._account_id = kwargs.get('obj').id if 'obj' in kwargs and kwargs.get('obj') else None

    def validate_name(self, field):
        account = Account.query.filter_by(name=field.data).first()
        if account and (self._account_id is None or account.id != self._account_id):
            raise ValidationError('Account name already exists.')
