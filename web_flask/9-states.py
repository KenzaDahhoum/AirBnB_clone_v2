#!/usr/bin/python3
"""
Starts a Flask web application to display a list of states and cities
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Displays a list of states"""
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays a list of cities for a specific state"""
    state = storage.get("State", id)
    if state:
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown(exception):
    """Closes the SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

