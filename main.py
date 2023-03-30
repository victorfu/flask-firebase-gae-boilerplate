import os
import logging
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, Response

app = Flask(__name__)

filename = "firebase-admin.json"
if os.path.exists(filename):
    cred = credentials.Certificate(filename)
    firebaseApp = firebase_admin.initialize_app(cred)
    db = firestore.client()

sql001 = "https://info.nhi.gov.tw/api/inae1000/inae1000s01/SQL001"
sql100 = "https://info.nhi.gov.tw/api/inae1000/inae1000s01/SQL100"
sql002 = "https://info.nhi.gov.tw/api/inae1000/inae1000s01/SQL002"
sql300 = "https://info.nhi.gov.tw/api/inae1000/inae1000s00/SQL300"


@app.route("/")
def hello():
    return "hello"


@app.route("/api/sql001/", methods=["GET"])
def proxy_sql001():
    target_url = sql001
    response = requests.get(target_url, params=request.args)
    return Response(response.content, response.status_code, response.headers.items())


@app.route("/api/sql100", methods=["POST"])
def proxy_sql100():
    target_url = sql100
    response = requests.post(target_url, json=request.get_json())
    return Response(response.content, response.status_code, response.headers.items())


@app.route("/api/sql002", methods=["POST"])
def proxy_sql002():
    target_url = sql002
    response = requests.post(target_url, json=request.get_json())
    return Response(response.content, response.status_code, response.headers.items())


@app.route("/api/sql300", methods=["POST"])
def proxy_sql300():
    target_url = sql300
    response = requests.post(target_url, json=request.get_json())
    return Response(response.content, response.status_code, response.headers.items())


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
