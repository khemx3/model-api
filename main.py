from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
from model import model
from dotenv import load_dotenv
import os



ml_model = model(20, 12)
ml_model.restore_model("models/model_10_weights")

app = Flask(__name__)
port = int(os.environ.get("PORT", 8000))


load_dotenv()

ENV_KEYS = {
    "type": "service_account",
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
     "auth_uri": os.environ.get("FIREBASE_AUTH_URI")
}


cred = credentials.Certificate(ENV_KEYS)
default_app = initialize_app(cred)
db = firestore.client()
stock_ref = db.collection('stock')

@app.route('/')
def hello_world():
    return "hello world"

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