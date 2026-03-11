from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("model/dropout_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    attendance = float(data["attendance"])
    study_hours = float(data["study_hours"])
    assignments = float(data["assignments"])
    gpa = float(data["gpa"])
    participation = float(data["participation"])

    # Risk score calculation
    risk_score = (100 - attendance) + (6 - study_hours) * 5 + (100 - assignments) * 0.5 + (10 - gpa) * 3

    if risk_score < 80:
        result = "LOW RISK"
    elif risk_score < 140:
        result = "MODERATE RISK"
    else:
        result = "HIGH RISK"

    return jsonify({"prediction": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)