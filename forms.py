from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class CreateForm(FlaskForm):

    name = StringField('Name of Account: ', [InputRequired()])
    balance = FloatField('Opening balance (optional)')
    password = PasswordField('Account password', [InputRequired(), EqualTo('pwd_confirm', message='Passwords must match')])
    pwd_confirm = PasswordField('Confirm account password')
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):

    id = IntegerField('Account ID: ', [InputRequired()])
    password = PasswordField('Account password: ', [InputRequired()])
    submit = SubmitField('Login')

class WithdrawForm(FlaskForm):

    amount = FloatField('Withdraw Amount: ', [InputRequired()])
    withdraw = SubmitField('Withdraw Amount')

class DepositForm(FlaskForm):

    amount = FloatField('Deposit Amount: ', [InputRequired()])
    deposit = SubmitField('Deposit Amount')

class TransferForm(FlaskForm):

    account_id = IntegerField("Recipient's Account ID: ", [InputRequired()])
    amount = FloatField('Transfer Amount: ', [InputRequired()])
    password = PasswordField('Account password: ', [InputRequired()])
    transfer = SubmitField('Transfer Amount')

class DeleteForm(FlaskForm):

    id = IntegerField('Account ID to Delete: ', [InputRequired()])
    password = PasswordField('Account password: ', [InputRequired(), EqualTo('pwd_confirm', message='Passwords must match')])
    pwd_confirm = PasswordField('Confirm account password: ')
    submit = SubmitField('Delete Account')
