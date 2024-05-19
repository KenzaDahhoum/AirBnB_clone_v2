#!/usr/bin/python3
""" Script to start a Flask web application with multiple routes """

from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_world():
     """ Returns 'Hello HBNB!' """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hello():
     """ Returns 'HBNB' """
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
     """ Returns 'C ' followed by the value of the text variable """
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/')
@app.route('/python/<text>')
def python_text(text='is cool'):
    """ Returns 'Python ' followed by the value of the text variable """
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
