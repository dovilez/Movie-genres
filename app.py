import datetime
import os
import pickle
import json
import psycopg2
from flask import Flask, request
import numpy as np
from train_model import clean_text, remove_stopwords

SAVED_MODEL_PATH = "model/classifier.pkl"
SAVED_BINARIZER_PATH = "model/binarizer.pkl"
SAVED_VECTORIZER_PATH = "model/vectorizer.pkl"

classifier = pickle.load(open(SAVED_MODEL_PATH, "rb"))
binarizer = pickle.load(open(SAVED_BINARIZER_PATH, "rb"))
vectorizer = pickle.load(open(SAVED_VECTORIZER_PATH, "rb"))


db_connection = psycopg2.connect(
    database=os.environ["DATABASE_NAME"],
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
    host=os.environ["DATABASE_HOST"],
    port=os.environ["DATABASE_PORT"],
)

app = Flask(__name__)


def __process_input(request_data: str) -> np.array:
    """
    Loads data from json and cleans the text
    :param request_data: input data
    :return: input data as a clean array
    """
    inputs = json.loads(request_data)["input"]
    inputs = [clean_text(item) for item in inputs]
    inputs = [remove_stopwords(item) for item in inputs]
    return inputs


@app.route("/predict", methods=["POST"])
def predict() -> str:
    """predict the movie genres based on the request data"""
    cur = db_connection.cursor()
    try:
        input_params = __process_input(request.data)
        input_vec = vectorizer.transform(input_params)
        prediction = classifier.predict(input_vec)
        predictions = binarizer.inverse_transform(prediction)
        for count, i in enumerate(input_params):
            pred = ", ".join(predictions[count])
            cur.execute(
                f"INSERT INTO prediction(input, output, time) VALUES('{i}', '{pred}', '{datetime.datetime.now()}' )"
            )
        db_connection.commit()

    except Exception as e:
        response = app.response_class(
            response=json.dumps({"error": f"{e.__class__} occured"}), status=400
        )
        return response

    response = app.response_class(
        response=json.dumps({"predictions:": binarizer.inverse_transform(prediction)}),
        status=200,
    )
    return response


@app.route("/recent", methods=["GET"])
def recent() -> str:
    """Show 10 most recent requests and responses"""
    cur = db_connection.cursor()
    cur.execute("SELECT *  FROM prediction ORDER BY time DESC LIMIT 10")
    rows = cur.fetchall()
    predictions = [{"input": row[1], "output": row[2]} for row in rows]
    return json.dumps({"predictions": predictions})
