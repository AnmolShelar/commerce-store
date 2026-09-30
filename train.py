import os
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
mlflow.set_experiment("E-Commerce Demand Forecast")

prices = np.array([[25], [50], [75], [100], [125], [150], [175], [200]])
sales = np.array([96, 88, 79, 71, 62, 54, 45, 37])

model = LinearRegression()
model.fit(prices, sales)
mae = mean_absolute_error(sales, model.predict(prices))

with mlflow.start_run() as run:
    mlflow.log_param("model", "LinearRegression")
    mlflow.log_param("training_rows", len(prices))
    mlflow.log_metric("mean_absolute_error", mae)
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="EcommerceDemand"
    )
    print(f"Trained model run: {run.info.run_id}; MAE: {mae:.2f}")
