import os
import joblib
import logging
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from category_encoders import TargetEncoder
from sklearn.model_selection import train_test_split
from pipeline.data_loader import load_data, clean_data

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Define paths
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)


def main():
    logging.info("Starting training process")

    # Load and clean data
    df = load_data()
    df = clean_data(df)

    target = "price"
    categorical_cols = ["type", "sector"]
    numerical_cols = [col for col in df.columns if col not in categorical_cols + [target]]
    train_cols = categorical_cols + numerical_cols

    X_train, X_valid, y_train, y_valid = train_test_split(
        df[train_cols], df[target], test_size=0.2, random_state=42, shuffle=True
    )
    # Preprocessing with encoding applied to categorical columns and passthrough to numerical ones
    preprocessor = ColumnTransformer([
        ("cat", TargetEncoder(), categorical_cols),
        ("num", "passthrough", numerical_cols)
    ])
    # Pipeline with model selected and tuned hyperparameters
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", GradientBoostingRegressor(
            learning_rate=0.1,
            n_estimators=300,
            max_depth=7,
            loss="absolute_error"
        ))
    ])

    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, MODEL_DIR / "model.pkl")

    logging.info("Model trained and saved")


if __name__ == "__main__":
    main()
