import os
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)

filename = "firebase-admin.json"
if os.path.exists(filename):
    cred = credentials.Certificate(filename)
    firebaseApp = firebase_admin.initialize_app(cred)
    db = firestore.client()


@app.route("/")
def hello():
    return "hello"


@app.route("/api/ping")
@cross_origin(send_wildcard=True)
def ping():
    return "pong"


@app.route("/api/firebase/<collection>")
def get_collection(collection):
    if db is None:
        return "db is None"

    docs = db.collection(collection).stream()
    output = []
    for doc in docs:
        dictDoc = doc.to_dict()
        dictDoc["id"] = doc.id
        output.append(dictDoc)
    return output


@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500
