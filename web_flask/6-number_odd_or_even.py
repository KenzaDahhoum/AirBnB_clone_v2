#!/usr/bin/python3
"""Script to start a Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def hello():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'

@app.route('/hbnb')
def hbnb():
    """Displays 'HBNB'"""
    return 'HBNB'

@app.route('/c/<text>')
def c(text):
    """Displays 'C ' followed by the value of the text variable"""
    text = text.replace('_', ' ')
    return 'C {}'.format(text)

@app.route('/python/')
@app.route('/python/<text>')
def python(text='is cool'):
    """Displays 'Python ' followed by the value of the text variable"""
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)

@app.route('/number/<int:n>')
def number(n):
    """Displays 'n is a number' only if n is an integer"""
    return '{} is a number'.format(n)

@app.route('/number_template/<int:n>')
def number_template(n):
    """Displays an HTML page with H1 tag containing 'Number: n'"""
    return render_template('6-number.html', n=n)

@app.route('/number_odd_or_even/<int:n>')
def number_odd_or_even(n):
    """Displays an HTML page with H1 tag containing 'Number: n is even|odd'"""
    if n % 2 == 0:
        odd_or_even = "even"
    else:
        odd_or_even = "odd"
    return render_template('6-number_odd_or_even.html', n=n, odd_or_even=odd_or_even)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

