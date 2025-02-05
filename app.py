from flask import Flask, request, jsonify
from flask_cors import CORS
import aiohttp
import asyncio
import os

app = Flask(__name__)
CORS(app)

# Helper functions
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number):
    return number == sum(i for i in range(1, number) if number % i == 0)

def is_armstrong(number):
    digits = [int(d) for d in str(number)]
    return number == sum(d**len(digits) for d in digits)

# Asynchronous function to fetch fun fact
async def fetch_fun_fact(number):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://numbersapi.com/{number}/math", timeout=5) as response:
                return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return "Fun fact unavailable."

@app.route('/api/classify-number', methods=['GET'])
async def classify_number():
    number_param = request.args.get('number')

    # Input validation
    try:
        number = int(number_param)
    except (TypeError, ValueError):
        return jsonify({"number": number_param, "error": True}), 400

    # Calculate properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    # Fetch digit sum
    digit_sum = sum(int(d) for d in str(number))

    # Fetch fun fact asynchronously
    fun_fact = await fetch_fun_fact(number)

    # Create response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    return jsonify(response), 200

if __name__ == "__main__":
    # Use the PORT environment variable provided by Render or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
