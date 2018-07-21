from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField



class CreateForm(FlaskForm):

    name = StringField('Name of Account:')
    balance = FloatField('Opening balance (optional)')
    password = PasswordField('Account password')
    pwd_confirm = PasswordField('Confirm account password')
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):

    id = IntegerField('Account ID: ')
    password = PasswordField('Account password: ')
    submit = SubmitField('Login')

class WithdrawForm(FlaskForm):

    amount = FloatField('Withdraw Amount: ')
    submit = SubmitField('Withdraw Amount')

class DepositForm(FlaskForm):

    amount = FloatField('Deposit Amount: ')
    submit = SubmitField('Deposit Amount')

class TransferForm(FlaskForm):

    account_id = IntegerField("Recipient's Account ID: ")
    amount = FloatField('Transfer Amount: ')
    password = PasswordField('Account password: ')
    submit = SubmitField('Transfer Amount')

class DeleteForm(FlaskForm):

    id = IntegerField('Account ID to Delete: ')
    password = PasswordField('Account password: ')
    pwd_confirm = PasswordField('Confirm account password: ')
    submit = SubmitField('Delete Account')
