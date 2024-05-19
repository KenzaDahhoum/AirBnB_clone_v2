#!/usr/bin/python3
""" 
4. Add fourth view function that displays var only if it is an integer 
"""

from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_world():
    """ Returns some text. """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hello():
    """ Return other text. """
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
    """ Replace underscores with spaces in text. """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/')
@app.route('/python/<text>')
def python_text(text='is cool'):
    """ Replace underscores with spaces in text. """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def number_text(n):
    """ Display n is a number if n is an integer. """
    return '{} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

