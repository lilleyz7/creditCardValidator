from flask import Flask, request, render_template
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
        valid, card_type = validate_card(number)
        if valid:
            return render_template('home.html', submit=True, number=number, is_valid=True, ctype=card_type)
        else:
            return render_template('home.html', submit=True, number=number, is_valid=False)
