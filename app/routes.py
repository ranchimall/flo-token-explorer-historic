from flask import render_template
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Balance requested for address {}'.format(
            form.address.data))
        return redirect(url_for('index'))
    return render_template('index.html', title='RMT', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Search', form=form)

@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Balance requested for address {}'.format(form.address.data))
        return 'string'
        # return redirect(url_for('index'))
    return render_template('test.html', form=form)