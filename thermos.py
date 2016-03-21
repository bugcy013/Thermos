__author__ = 'dhana013'


from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import datetime
from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

bookmarks = []
app.config['SECRET_KEY'] = "\xde:~\xf7\xdd\n%\x8f\x86\xec\xdc8\x9f\xa0\xc0\x9c\x83,\x8ee\x90' \x8d"


def store_bookmark(url):
    bookmarks.append(dict(
        url=url,
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
def index():
    return render_template('index.html', title='values passed from program', user=User("Dhanaskekaran", "Anbalagan"))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        url = request.form['url']
        store_bookmark(url)
        # app.logger.debug('stored_url: ' + url)
        flash("store_bookmark '{}'".format(url))
        return redirect(url_for('index'))

    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)