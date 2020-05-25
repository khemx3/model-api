from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
from model import model
import os


ml_model = model(20, 12)
ml_model.restore_model("models/model_10_weights")

app = Flask(__name__)
port = int(os.environ.get("PORT", 8000))
 

cred = credentials.Certificate(Buffer.from(process.env.FIREBASE_CONFIG_BASE64, 'base64').toString('ascii')))
default_app = initialize_app(cred)
db = firestore.client()
stock_ref = db.collection('stock')

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

@app.route('/backtest/run', methods=['GET'])
def generatebacktest():
    return 'Generating Backtest'


@app.route('/backtest/<name>', methods=['GET'])
def read(name):
    try:
        stock_name = name
        if stock_name:
            stock = stock_ref.document(stock_name).get()
            return jsonify(stock.to_dict()), 200
        else:
            stock = [doc.to_dict() for doc in stock_ref.stream()]
            return jsonify(stock), 200
        
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=port)