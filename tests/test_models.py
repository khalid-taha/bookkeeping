# tests/test_models.py

from datetime import date

def test_transaction_model(db):
    from modules.models.account import Account
    from modules.models.transaction import Transaction

    # Add unique accounts
    debit_account = Account(name='Cash_Test', type='Asset')
    credit_account = Account(name='Revenue_Test', type='Revenue')

    db.session.add_all([debit_account, credit_account])
    db.session.commit()

    # Use date object for the date field
    transaction_date = date.today()

    # Create a transaction with date
    transaction = Transaction(
        date=transaction_date,
        debit_account_id=debit_account.id,
        credit_account_id=credit_account.id,
        amount=1000.00,
        description='Test Transaction'
    )

    db.session.add(transaction)
    db.session.commit()

    # Assertions
    assert transaction.id is not None
    assert transaction.date == transaction_date
    assert transaction.debit_account.name == 'Cash_Test'
    assert transaction.credit_account.name == 'Revenue_Test'
