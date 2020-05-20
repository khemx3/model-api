from flask import Flask, jsonify, request
from model import model
import os


ml_model = model(20, 12)
ml_model.restore_model("models/model_10_weights")

app = Flask(__name__)
port = int(os.environ.get("PORT", 8000))

@app.route('/')
def hello_world():
    return 'Flask Dockerized and deployed to Heroku'

@app.route("/model", methods=['POST'])
def generatemodel():
    data = request.get_json()
    inputVal = data["input"][:]
    input_window = ml_model.prepare_prediction_data(data["input"])
    pattern = ml_model.predict_pattern(input_window)

    return jsonify(
        name=data["name"],
        input=inputVal,
        output=pattern[0].tolist()
    )


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=port)