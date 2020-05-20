from flask import Flask, jsonify, request
from model import model


ml_model = model(20, 12)
ml_model.restore_model("app/models/model_10_weights")

app = Flask(__name__)


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
    app.run(host='0.0.0.0', debug=True, port=8000)