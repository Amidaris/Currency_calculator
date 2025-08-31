from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Pobierz dane z API
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates = data[0]['rates']

    # Lista kodów walut
    currency_codes = [rate['code'] for rate in rates]

    result = None

    if request.method == 'POST':
        selected_currency = request.form['currency']
        amount = float(request.form['amount'])

        # Znajdź kurs wybranej waluty
        rate = next((r for r in rates if r['code'] == selected_currency), None)
        if rate:
            cost_in_pln = amount * rate['ask']
            result = f"{amount} {selected_currency} kosztuje {cost_in_pln:.2f} PLN"

    return render_template('index.html', currency_codes=currency_codes, result=result)