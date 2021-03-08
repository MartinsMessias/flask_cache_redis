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
            f'Fibonacci sum for: {form.number.data} = {data}')
        return redirect('/')
    return render_template('base.html', title='Fibonacci Generator', form=form)


@app.route('/fibonacci/<number>', methods=['GET'])
def get_fibonacci(number):
    if int(number) > 10000:
        return jsonify(['Number must be between 1 and 10000'])
    data = get_fibonacci_sequence(int(number))

    if not data:
        return jsonify(['Enter a non-negative integer'])

    return jsonify({'fibonacci': data})


# Fibonacci function
def get_fibonacci_sequence(terms):
    """
    - Returns data like this
    False

    or 

    fibonacci_sum = 123
    """
    if cache.exists(str(terms)):
        print('redis get obj')
        fibonacci_sum = cache.get(terms).decode('utf-8')
        return fibonacci_sum
        
    n1, n2 = 0, 1
    count = 0

    fibonacci_sum = 0
    sequence = [0, 1]

    if terms <= 0:
        return False
    elif terms == 1:
        fibonacci_sum = n2
        cache.mset({terms: fibonacci_sum})
    else:
        while count <= terms:
            sequence.append(n1)
            nth = n1 + n2
            n1 = n2
            n2 = nth
            count += 1

        fibonacci_sum = sum(sequence)
        cache.mset({terms: fibonacci_sum})
    return fibonacci_sum


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)