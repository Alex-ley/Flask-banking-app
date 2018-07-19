import os
from datetime import datetime
from forms import  CreateForm , WithdrawForm, DepositForm, TransferForm, DeleteForm
from flask import Flask, session, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy import event
# from sqlalchemy import DDL

app = Flask(__name__)
# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'
############################################

        # SQL DATABASE AND MODELS

##########################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://alexley:MySQL_password@alexley.mysql.pythonanywhere-services.com/alexley$bank'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Account(db.Model):

    __tablename__ = 'accounts'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),unique=True)
    password = db.Column(db.Text) #To be HASHED
    balance = db.Column(db.Float)
    active = db.Column(db.Boolean,default=True)

    def __init__(self,name, password, balance=0):
        self.name = name
        self.password = password #To be HASHED
        self.balance = balance

    def __repr__(self):
        return f"Account name is {self.name} with account number {self.id}"

class Transaction(db.Model):

    __tablename__ = 'transactions'
    id = db.Column(db.Integer,primary_key = True)
    transaction_type = db.Column(db.Text)
    description = db.Column(db.Text)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    account_id = db.Column(db.Integer,db.ForeignKey('accounts.id'),nullable=False)
    account = db.relationship('Account',backref=db.backref('transactions', lazy=True))

    def __init__(self,transaction_type, description, account_id, amount=0):
        self.transaction_type = transaction_type
        self.description = description
        self.account_id = account_id
        self.amount = amount

    def __repr__(self):
        return f"Transaction {self.id} on {self.date}"

# event.listen(
#     Account.__table__,
#     "after_create",
#     DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10000001;")
# )
############################################

        # VIEWS WITH FORMS

##########################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateForm()

    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data #To be HASHED
        if form.balance.data > 0:
            balance = form.balance.data
        else:
            balance = 0

        # Add new bank account to database
        new_account = Account(name,password,balance)
        db.session.add(new_account)
        db.session.commit()
        new_transaction = Transaction('deposit','account opening',new_account.id,balance)
        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for('my_account'))

    return render_template('create_account.html',form=form)

@app.route('/list_accounts')
def list_accounts():
    # Grab a list of accounts from database.
    accounts = Account.query.all()
    return render_template('list_accounts.html', accounts=accounts)

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    withdraw_form = WithdrawForm()
    deposit_form = DepositForm()
    transfer_form = TransferForm()
    transactions = Transaction.query.all()

    if form.validate_on_submit():
        id = form.id.data
        password = form.id.data #To be HASHED
        account = Account.query.get(id)
        if account.password == password:
            db.session.delete(account)
            db.session.commit()
            return redirect(url_for('list_accounts'))
        else:
            return '<h1>Invalid Account ID & Password combination</h1>'

    return render_template('my_account.html',transactions=transactions,withdraw_form=withdraw_form,deposit_form=deposit_form,transfer_form=transfer_form)

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.id.data #To be HASHED
        account = Account.query.get(id)
        if account.password == password:
            db.session.delete(account)
            db.session.commit()
            return redirect(url_for('list_accounts'))
        else:
            return '<h1>Invalid Account ID & Password combination</h1>'

    return render_template('delete_account.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
