import os

# Required
API_KEY = os.environ.get("API_KEY")

# Model path (used by inference code)
MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.pkl")

# Optional data source selector
DATA_SOURCE = os.environ.get("DATA_SOURCE", "csv")

# Only used if DATA_SOURCE=database
DB_CONN_STRING = os.environ.get("DB_CONN_STRING")
TRAIN_QUERY = os.environ.get("TRAIN_QUERY", "SELECT * FROM properties_train")
TEST_QUERY = os.environ.get("TEST_QUERY", "SELECT * FROM properties_test")