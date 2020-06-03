from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app

from backtrack import backtrack, model_input
from dotenv import load_dotenv
import os
import json


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
    pattern = model_input(inputVal)

    return jsonify(
        name=data["name"],
        input=inputVal,
        output=pattern[0].tolist()
    )

@app.route('/backtest/run/<name>', methods=['GET'])
def generatebacktest(name):
    try:
        temp = backtrack(name)
        stock_ref.document(name).set({
                u'data':temp[1],
                u'label':temp[0],
                u'name':name
            }
        )
        return name
    except Exception as e:
        return f"An Error Occured: {e}"
    


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