# [START app]
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask

app = Flask(__name__)

cred = credentials.Certificate("firebase-admin.json")
firebaseApp = firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route("/")
def hello():
    return "Hello!"


@app.route("/api/<collection>")
def get_collection(collection):
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


# [END app]
