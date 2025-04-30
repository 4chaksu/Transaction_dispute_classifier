from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_eligibility(data):
    income = data.get("income", 0)
    employment_status = data.get("employment_status", "unemployed").lower()
    existing_loans = data.get("existing_loans", 0)

    # logic for scoring
    score = 0

    if income > 50000:
        score += 40
    elif income > 30000:
        score += 30
    else:
        score += 10

    if employment_status == "employed":
        score += 40
    elif employment_status == "self-employed":
        score += 30
    else:
        score += 10

    if existing_loans == 0:
        score += 20
    elif existing_loans < 2:
        score += 10
    else:
        score += 0

    # recommendation
    if score >= 80:
        recommendation = "Eligible for loan with best terms."
    elif score >= 50:
        recommendation = "Eligible with standard terms."
    else:
        recommendation = "Not eligible currently. Try again later."

    return score, recommendation

@app.route("/loan-eligibility", methods=["POST"])
def loan_eligibility():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    score, recommendation = calculate_eligibility(data)

    return jsonify({
        "eligibility_score": score,
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(debug=True)
