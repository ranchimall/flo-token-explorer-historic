from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import SearchForm, BlankForm
import sqlite3
import json
import os

dbfolder = '/home/production/deployed/flo-token-tracking/tokens/'


@app.route('/')
def redirectRMT():
    return redirect('/rmt')


@app.route('/<token>', methods=['GET', 'POST'])
def index(token):
    if token is None:
        token = 'rmt'
    form = SearchForm()
    dblocation = dbfolder + token + '.db'
    if os.path.exists(dblocation):
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
    else:
        return 'Token doesn\'t exist'
    c.execute(
        'SELECT id, blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory ORDER BY id DESC LIMIT 5')
    transactionHistoryTable = c.fetchall()
    c.execute('SELECT address,SUM(transferBalance) FROM activeTable GROUP BY address')
    balanceTable = c.fetchall()
    conn.close()

    if form.validate_on_submit():
        flash('Balance requested for address {}'.format(form.address.data))
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
        c.execute("select SUM(transferBalance) from activeTable WHERE address=='{}'".format(str(form.address.data)))
        balance = c.fetchall()[0][0]
        c.execute(
            'SELECT id, blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory ORDER BY id DESC LIMIT 5')
        transactionHistoryTable = c.fetchall()
        c.execute('SELECT address,SUM(transferBalance) FROM activeTable GROUP BY address')
        balanceTable = c.fetchall()
        conn.close()
        return render_template('index.html', form=form, balance=balance,
                               transactionHistoryTable=transactionHistoryTable, balanceTable=balanceTable, token=token)

    return render_template('index.html', form=form, transactionHistoryTable=transactionHistoryTable,
                           balanceTable=balanceTable, token=token)


@app.route('/<token>/transactions', methods=['GET', 'POST'])
def transactions(token):
    sourceFloAddress = request.args.get('sourceFloAddress')
    destFloAddress = request.args.get('destFloAddress')
    if token is None:
        token = 'rmt'

    dblocation = dbfolder + token + '.db'

    if None not in [sourceFloAddress, destFloAddress]:
        if os.path.exists(dblocation):
            conn = sqlite3.connect(dblocation)
            c = conn.cursor()
        else:
            return 'Token doesn\'t exist'
        if sourceFloAddress and not destFloAddress:
            c.execute('SELECT id, blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory WHERE sourceFloAddress="{}" ORDER BY id DESC'.format(
                sourceFloAddress))
        if not sourceFloAddress and destFloAddress:
            c.execute(
                'SELECT id, blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory WHERE destFloAddress="{}" ORDER BY id DESC'.format(destFloAddress))
        if sourceFloAddress and destFloAddress:
            c.execute(
                'SELECT id, blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory WHERE sourceFloAddress="{}" OR destFloAddress="{}" ORDER BY id DESC'.format(
                    sourceFloAddress, destFloAddress))

        transactionHistoryTable = c.fetchall()
        conn.close()
        return render_template('transactions.html', transactionHistoryTable=transactionHistoryTable, token=token)
    if os.path.exists(dblocation):
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
    else:
        return 'Token doesn\'t exist'
    c.execute(
        'SELECT id, blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory ORDER BY id DESC')
    transactionHistoryTable = c.fetchall()
    conn.close()
    return render_template('transactions.html', token=token, transactionHistoryTable=transactionHistoryTable)


@app.route('/api/v1.0/getaddressbalance', methods=['GET'])
def getaddressbalance():
    address = request.args.get('address')
    token = request.args.get('token')

    if address is None or token is None:
        return jsonify(result='error')

    dblocation = dbfolder + token + '.db'
    if os.path.exists(dblocation):
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
    else:
        return 'Token doesn\'t exist'
    c.execute('SELECT SUM(transferBalance) FROM activeTable WHERE address="{}"'.format(address))
    balance = c.fetchall()[0][0]
    conn.close()
    return jsonify(result='ok', token=token, address=address, balance=balance)


@app.route('/api/v1.0/gettokeninfo', methods=['GET'])
def gettokeninfo():
    token = request.args.get('token')

    if token is None:
        return jsonify(result='error')

    dblocation = dbfolder + token + '.db'
    if os.path.exists(dblocation):
        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
    else:
        return 'Token doesn\'t exist'
    c.execute('SELECT * FROM transactionHistory WHERE id=1')
    incorporationRow = c.fetchall()[0]
    c.execute('SELECT COUNT (DISTINCT address) FROM activeTable')
    numberOf_distinctAddresses = c.fetchall()[0][0]
    conn.close()
    return jsonify(result='ok', token=token, incorporationAddress=incorporationRow[2], tokenSupply=incorporationRow[3],
                   transactionHash=incorporationRow[6], blockchainReference=incorporationRow[7],
                   activeAddress_no=numberOf_distinctAddresses)


@app.route('/api/v1.0/gettransactions', methods=['GET'])
def gettransactions():
    token = request.args.get('token')
    senderFloAddress = request.args.get('senderFloAddress')
    destFloAddress = request.args.get('destFloAddress')

    if token is None:
        return jsonify(result='error')

    dblocation = dbfolder + token + '.db'
    if os.path.exists(dblocation):
        conn = sqlite3.connect(dblocation)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
    else:
        return 'Token doesn\'t exist'

    if senderFloAddress and not destFloAddress:
        c.execute(
            'SELECT blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory WHERE sourceFloAddress="{}" ORDER BY id DESC LIMIT 100'.format(
                senderFloAddress))
    if not senderFloAddress and destFloAddress:
        c.execute(
            'SELECT blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory WHERE destFloAddress="{}" ORDER BY id DESC LIMIT 100'.format(
                destFloAddress))
    if senderFloAddress and destFloAddress:
        c.execute(
            'SELECT blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory WHERE sourceFloAddress="{}" OR destFloAddress="{}" ORDER BY id DESC LIMIT 100'.format(
                senderFloAddress, destFloAddress))

    else:
        c.execute(
            'SELECT blockNumber, sourceFloAddress, destFloAddress, transferAmount, blockchainReference FROM transactionHistory ORDER BY id DESC LIMIT 100')
    latestTransactions = c.fetchall()
    conn.close()
    rowarray_list = []
    for row in latestTransactions:
        d = dict(zip(row.keys(), row))  # a dict with column names as keys
        rowarray_list.append(d)
    return jsonify(result='ok', transactions=rowarray_list)


@app.route('/test')
def test():
    return render_template('test.html')

