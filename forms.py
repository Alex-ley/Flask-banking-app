from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField



class AddForm(FlaskForm):

    name = StringField('Name of Account:')
    balance = FloatField('Opening balance (optional)')
    password = PasswordField('Account password')
    submit = SubmitField('Create Account')

class ModifyForm(FlaskForm):

    account_id = IntegerField("Account ID")
    ammount = FloatField('Deposit / Withdraw Ammount')
    deposit = SubmitField('Deposit Ammount')
    withdraw = SubmitField('Withdraw Ammount')

class DelForm(FlaskForm):

    id = IntegerField('Account ID to Delete:')
    submit = SubmitField('Delete Account')
