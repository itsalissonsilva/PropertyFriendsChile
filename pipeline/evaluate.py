import os
import joblib
import logging
from dotenv import load_dotenv
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from pipeline.data_loader import load_data, clean_data
import numpy as np

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def evaluate():
    logging.info("Loading test data for evaluation")

    df = load_data(load_test_only=True)
    df = clean_data(df)

    model = joblib.load("models/model.pkl")

    X_test = df.drop(columns=["price"])
    y_true = df["price"]
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)

    logging.info(f" MAE: {mae:.2f}")
    logging.info(f" RMSE: {rmse:.2f}")
    logging.info(f" MAPE: {mape:.4f}")


if __name__ == "__main__":
    evaluate()
