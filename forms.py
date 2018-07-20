from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField



class CreateForm(FlaskForm):

    name = StringField('Name of Account:')
    balance = FloatField('Opening balance (optional)')
    password = PasswordField('Account password')
    pwd_confirm = PasswordField('Confirm account password')
    submit = SubmitField('Create Account')

class WithdrawForm(FlaskForm):

    ammount = FloatField('Withdraw Ammount')
    withdraw = SubmitField('Withdraw Ammount')

class DepositForm(FlaskForm):

    ammount = FloatField('Withdraw Ammount')
    deposit = SubmitField('Deposit Ammount')

class TransferForm(FlaskForm):

    account_id = IntegerField("Recipient's Account ID")
    ammount = FloatField('Transfer Ammount')
    password = PasswordField('Account password')
    transfer = SubmitField('Transfer Ammount')

class DeleteForm(FlaskForm):

    id = IntegerField('Account ID to Delete:')
    password = PasswordField('Account password')
    pwd_confirm = PasswordField('Confirm account password')
    submit = SubmitField('Delete Account')
