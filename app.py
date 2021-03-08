from flask import render_template, flash, redirect
from flask.json import jsonify
from flask.wrappers import Response

from settings import app, cache
from forms import FiboForm
import json


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FiboForm()
    if form.validate_on_submit():
        data = get_fibonacci_sequence(form.number.data)
        if not data:
            flash('Enter a non-negative integer')
            return redirect('/')
        flash(
            f'Fibonacci: {form.number.data} = {data["fibonacci"]}')
        return redirect('/')
    return render_template('base.html', title='Fibonacci Generator', form=form)


@app.route('/fibonacci/<number>', methods=['GET'])
def get_fibonacci(number):
    if int(number) > 2000:
        return jsonify(['Number must be between 1 and 2000'])
    data = get_fibonacci_sequence(int(number))

    if not data:
        return jsonify(['Enter a non-negative integer'])

    return jsonify(data)


# Fibonacci function
def get_fibonacci_sequence(terms):
    """
    - Returns data like this
    False

    or 

    data = {
        fibonacci: 12,
        sequence: [0, 1, 1, 2, 3, 5],
    }
    """
    if cache.exists(str(terms)):
        print('redis get obj')
        return json.loads(cache.get(str(terms)).decode('utf-8').replace("\'", "\""))
        
    n1, n2 = 0, 1
    count = 1

    data = {}
    sequence = []

    if terms < 0:
        return False
    elif terms == 1:
        data["fibonacci"] = n2
        cache.mset({str(terms): json.dumps(data)})
    else:
        while count <= terms:
            sequence.append(n1)
            nth = n1 + n2
            n1 = n2
            n2 = nth
            count += 1

        data["fibonacci"] = sum(sequence)
        cache.mset({str(terms): json.dumps(data)})
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)