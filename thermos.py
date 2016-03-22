__author__ = 'dhana013'


from flask import Flask, render_template, url_for, request, redirect, flash, session
from datetime import datetime
from logging import DEBUG
from functools import wraps


app = Flask(__name__)
app.logger.setLevel(DEBUG)

bookmarks = []
app.config['SECRET_KEY'] = "\xde:~\xf7\xdd\n%\x8f\x86\xec\xdc8\x9f\xa0\xc0\x9c\x83,\x8ee\x90' \x8d"

from forms import BookmarkForm

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user='reindert',
        date=datetime.utcnow()
    ))

def new_bookmark(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


class User(object):
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return "{}.{}".format(self.firstname[0], self.lastname[0])

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', new_bookmarks=new_bookmark(5))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        # app.logger.debug('stored_url: ' + url)
        flash("store_bookmark '{}'".format(description))
        return redirect(url_for('index'))

    return render_template('add.html', form=form)


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("You were just logged in")
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("You were just logged out")
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)