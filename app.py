import os
from datetime import datetime
from forms import  CreateForm, LoginForm, WithdrawForm, DepositForm, TransferForm, DeleteForm
from flask import Flask, session, render_template, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
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

    def deposit_withdraw(self,type,amount):
        if type == 'withdraw':
            amount *= -1
        if self.balance + amount < 0:
            return False #Unsuccessful
        else:
            self.balance += amount
            return True #Successful

    def __init__(self,name, password, balance=0):
        self.name = name
        self.password = generate_password_hash(password) #HASHED
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
        return f"Transaction {self.id}: {self.transaction_type} on {self.date}"

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
        session['username'] = new_account.name

        return redirect(url_for('my_account'))

    return render_template('create_account.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data #To be HASHED
        account = Account.query.get(id)
        if check_password_hash(account.password,password):
            session['username'] = account.name
            return redirect(url_for('my_account'))
        else:
            return '<h1>Invalid Account ID & Password combination</h1>'

    return render_template('login.html',form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = None
    return redirect(url_for('index'))

@app.route('/json/account/name/<name>')
def json_names(name):
    # accounts = Account.query.all() #.options(load_only('name'))
    # names_list = []
    # for account in accounts:
    #     names_list.append(account.name)
    # return jsonify({'names': names_list})
    if Account.query.filter_by(name=name).first():
        return jsonify({'name': 'taken'})
    else:
        return jsonify({'name': 'available'})

@app.route('/json/account/id/<account_id>')
def json_account_id(account_id):
    if Account.query.filter_by(id=account_id).first():
        return jsonify({'account': 'valid account ID'})
    else:
        return jsonify({'account': 'invalid account ID'})

@app.route('/list_accounts')
def list_accounts():
    # Grab a list of accounts from database.
    accounts = Account.query.filter_by(active=True)
    return render_template('list_accounts.html', accounts=accounts)

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    withdraw_form = WithdrawForm()
    deposit_form = DepositForm()
    transfer_form = TransferForm()
    user = session['username']
    account = Account.query.filter_by(name=user).first()
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.date.desc())

    if deposit_form.deposit.data and deposit_form.validate():
        id = account.id
        amount = deposit_form.amount.data
        account = Account.query.get(id)
        if account.deposit_withdraw('deposit',amount):
            new_transaction = Transaction('deposit','self deposit',account.id,amount)
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('my_account'))
        else:
            #flash = you do not have sufficient funds to perform this operation
            return redirect(url_for('my_account'))
    elif withdraw_form.withdraw.data and withdraw_form.validate():
        id = account.id
        amount = withdraw_form.amount.data
        account = Account.query.get(id)
        if account.deposit_withdraw('withdraw',amount):
            amount *= -1
            new_transaction = Transaction('withdraw','self withdraw',account.id,amount)
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('my_account'))
        else:
            #flash = you do not have sufficient funds to perform this operation
            return redirect(url_for('my_account'))
    elif transfer_form.transfer.data and transfer_form.validate():
        id = account.id
        amount = transfer_form.amount.data
        account_id = transfer_form.account_id.data
        password = transfer_form.password.data #To be HASHED
        account = Account.query.get(id)
        if check_password_hash(account.password,password):
            if account.deposit_withdraw('withdraw',amount):
                amount *= -1
                new_transaction = Transaction('transfer out',f'transfer to account {account_id}',account.id,amount)
                db.session.add(new_transaction)
                recipient = Account.query.get(account_id)
                if recipient.deposit_withdraw('deposit',amount):
                    new_transaction2 = Transaction('transfer in',f'transfer from account {account.id}',account_id,amount)
                    db.session.add(new_transaction2)
                    db.session.commit()
                    return redirect(url_for('my_account'))
                else:
                    #flash = you do not have sufficient funds to perform this operation
                    return redirect(url_for('my_account'))
            else:
                #flash = you do not have sufficient funds to perform this operation
                return redirect(url_for('my_account'))
        else:
            return '<h1>Invalid Account Password</h1>'

    return render_template('my_account.html',user=user,account=account,transactions=transactions,withdraw_form=withdraw_form,deposit_form=deposit_form,transfer_form=transfer_form)

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data #To be HASHED
        account = Account.query.get(id)
        if check_password_hash(account.password,password):
            #db.session.delete(account)
            account.active = False
            db.session.commit()
            return redirect(url_for('list_accounts'))
        else:
            return redirect(url_for('list_accounts')) #'<h1>Invalid Account ID & Password combination</h1>'

    return render_template('delete_account.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
