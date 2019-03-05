from flask import render_template
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import SearchForm, BlankForm
import sqlite3

dblocation = '/home/vivek/Documents/Ranchimall/flo-token-tracking/tree.db'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    blankform = BlankForm()
    conn = sqlite3.connect(dblocation)
    c = conn.cursor()
    c.execute('SELECT * FROM transactionHistory ORDER BY id DESC LIMIT 5')
    transactionHistoryTable = c.fetchall()
    c.execute('SELECT address,SUM(transferBalance) FROM transactiontable GROUP BY address')
    balanceTable = c.fetchall()
    conn.close()

    if form.validate_on_submit():
        flash('Balance requested for address {}'.format(form.address.data))
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
        c.execute("select SUM(transferBalance) from transactiontable WHERE address=='{}'".format(str(form.address.data)))
        balance = c.fetchall()[0][0]
        c.execute('SELECT * FROM transactionHistory ORDER BY id DESC LIMIT 5')
        transactionHistoryTable = c.fetchall()
        c.execute('SELECT address,SUM(transferBalance) FROM transactiontable GROUP BY address')
        balanceTable = c.fetchall()
        conn.close()
        return render_template('index.html', form=form, blankform=blankform, balance=balance, transactionHistoryTable=transactionHistoryTable, balanceTable=balanceTable)

    if blankform.validate_on_submit():
        return "str"
        flash('Balance requested for address {}'.format(form.address.data))
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
        c.execute("select SUM(transferBalance) from transactiontable WHERE address=='{}'".format(str(form.address.data)))
        balance = c.fetchall()[0][0]
        c.execute('SELECT * FROM transactionHistory ORDER BY id DESC LIMIT 5')
        transactionHistoryTable = c.fetchall()
        c.execute('SELECT address,SUM(transferBalance) FROM transactiontable GROUP BY address')
        balanceTable = c.fetchall()
        conn.close()
        return render_template('index.html', form=form, blankform=blankform, balance=balance, transactionHistoryTable=transactionHistoryTable, balanceTable=balanceTable)

    return render_template('index.html', form=form, blankform=blankform, transactionHistoryTable=transactionHistoryTable, balanceTable=balanceTable)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    address = request.args.get('address')
    if address is not None:
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
        c.execute('SELECT * FROM transactionHistory WHERE fromAddress="{}" OR toAddress="{}" ORDER BY id DESC'.format(address,address))
        transactionHistoryTable = c.fetchall()
        conn.close()
        return render_template('transactions.html', transactionHistoryTable=transactionHistoryTable)
    conn = sqlite3.connect(dblocation)
    c = conn.cursor()
    c.execute('SELECT * FROM transactionHistory ORDER BY id DESC')
    transactionHistoryTable = c.fetchall()
    conn.close()
    return render_template('transactions.html', transactionHistoryTable=transactionHistoryTable)

@app.route('/test')
def test():
    return render_template('test.html')

