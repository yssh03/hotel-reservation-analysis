from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import joblib
from config.path_config import MODEL_OUTPUT_PATH
import numpy as np

app = Flask(__name__)
CORS(app)
model = joblib.load(MODEL_OUTPUT_PATH)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    lead_time = int(data["lead_time"])
    market_segment_type = int(data["market_segment_type"])
    arrival_month = int(data["arrival_month"])
    arrival_date = int(data["arrival_date"])
    no_of_special_requests = int(data["no_of_special_requests"])
    no_of_week_nights = int(data["no_of_week_nights"])
    no_of_weekend_nights = int(data["no_of_weekend_nights"])
    type_of_meal_plan = int(data["type_of_meal_plan"])
    room_type_reserved = int(data["room_type_reserved"])
    avg_price_per_room = float(data["avg_price_per_room"])

    features = np.array(
        [[lead_time, no_of_special_requests, avg_price_per_room, arrival_month, arrival_date, market_segment_type, no_of_week_nights, no_of_weekend_nights, type_of_meal_plan, room_type_reserved]])
    prediction = model.predict(features)[0]
    prediction_mapping = {
        0: "This customer will not cancel this booking.",
        1: "This customer is likely to cancel this booking."
    }
    return jsonify({"prediction": prediction_mapping[prediction]}), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)
