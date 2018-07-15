import os
from forms import  AddForm , DelForm, AddOwnerForm
from flask import Flask, render_template, url_for, redirect
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alexley:MySQL_password@alexley.mysql.pythonanywhere-services.com/default'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Account(db.Model):

    __tablename__ = 'accounts'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    password = db.Column(db.Text) #To be HASHED
    balance = db.Column(db.Float)

    def __init__(self,name, password, balance=0):
        self.name = name
        self.password = password #To be HASHED
        self.balance = balance

    def __repr__(self):
        return f"Account name is {self.name} with account number {self.id}"

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

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = AddForm()

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

        return redirect(url_for('account'))

    return render_template('account.html',form=form)

@app.route('/list')
def list():
    # Grab a list of accounts from database.
    accounts = Account.query.all()
    return render_template('list.html', accounts=accounts)

@app.route('/delete', methods=['GET', 'POST'])
def del_account():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.id.data #To be HASHED
        account = Account.query.get(id)
        if account.password == password:
            db.session.delete(pup)
            db.session.commit()
            return redirect(url_for('list'))
        else:
            return <h1>Invalid Account ID & Password combination</h1>

    return render_template('delete.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
