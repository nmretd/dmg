from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# I have created this Function to get exchange rates from an API call
def get_exchange_rates(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("rates", {})
    return {}

@app.route("/", methods=["GET", "POST"])

# I am limiting the list of currencies to G10 but this can be extended if required
def index():
    G10_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF", "NOK", "SEK"}
    
    converted_amount = None
    conversion_msg = None
    error = None
    
    rates = get_exchange_rates("USD")  # I am setting the Default base currency to USD
    rates = {currency: rate for currency, rate in rates.items() if currency in G10_CURRENCIES}

    if request.method == "POST":
        amount = request.form.get("amount")
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")

        try:
            amount = float(amount)
            rates = get_exchange_rates(from_currency)
            rates = {currency: rate for currency, rate in rates.items() if currency in G10_CURRENCIES}

            if to_currency in rates:
                converted_amount = round(amount * rates[to_currency], 2)
                conversion_msg = f"{amount} {from_currency} = {converted_amount} {to_currency}"
            else:
                error = "Invalid currency selection."
        except ValueError:
            error = "Please enter a valid amount."

    return render_template(
        "index.html", 
        rates=rates, 
        converted_amount=converted_amount, 
        conversion_msg=conversion_msg,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
