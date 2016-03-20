__author__ = 'dhana013'


from flask import Flask, render_template, url_for

app = Flask(__name__)

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


@app.route('/add')
def add():
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)