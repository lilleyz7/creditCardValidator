from flask import Flask, jsonify, request, render_template, flash
from validator import validate_card
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("400/day;1/second")
def base_route():
    if request.method == 'GET':
        return render_template('home.html', submit=False)
    if request.method == 'POST':
        # handle validation
        number = request.form["cardNumber"]
        if number is None or len(number) < 8 or len(number) > 18:
            flash('Please enter a valid card number')
            return render_template('home.html')
        valid, card_company = validate_card(number)
        if valid:
            return render_template('home.html', submit=True, number=number, is_valid=True, ctype=card_company)
        else:
            return render_template('home.html', submit=True, number=number, is_valid=False)

@app.route('/api/<card_number>', methods=['GET', 'POST'])
def api_route(card_number):
    if card_number is None:
        error = {
            'error': 'card_number is required'
        }
        return jsonify(error)
    if len(card_number) > 18 or len(card_number) < 8:
        error = {
            'error': 'invalid length of card number'
        }
        return jsonify(error)
    
    else:
        is_valid, card_company = validate_card(card_number)
        if not is_valid:
            response = {
                'data': 'card is invalid'
            }
            return jsonify(response)
        response = {
            'data': 'card is valid',
            'carrier': card_company
        }
        return jsonify(response)
if __name__ == '__main__':
    app.run()