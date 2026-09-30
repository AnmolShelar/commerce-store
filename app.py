import os
import time
import numpy as np
import mlflow
import mlflow.pyfunc
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
model = mlflow.pyfunc.load_model("models:/EcommerceDemand/1")

app = Flask(__name__)
predictions = Counter("store_predictions_total", "Number of store demand predictions")
prediction_time = Histogram("store_prediction_seconds", "Prediction response time")

@app.get("/health")
def health():
    return jsonify({"status": "ok", "model": "EcommerceDemand version 1"})

@app.get("/predict")
def predict():
    price = float(request.args.get("price", "80"))
    started = time.time()
    demand = float(model.predict(np.array([[price]]))[0])
    prediction_time.observe(time.time() - started)
    predictions.inc()
    return jsonify({"price": price, "predicted_units": round(max(0, demand), 2)})

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
