import os
import logging
import pandas as pd
from sqlalchemy import create_engine

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_data(source="csv", train_path=None, test_path=None, load_test_only=False):
    source = os.getenv("DATA_SOURCE", source)

    if source == "csv":
        data_dir = "data"
        train_path = train_path or os.path.join(data_dir, "train.csv")
        test_path = test_path or os.path.join(data_dir, "test.csv")

        if load_test_only:
            logging.info("Loading test.csv only")
            return pd.read_csv(test_path)
        else:
            logging.info("Loading train.csv")
            return pd.read_csv(train_path)

    elif source == "database":
        conn_string = os.environ["DB_CONN_STRING"]
        engine = create_engine(conn_string)

        if load_test_only:
            query = os.environ.get("TEST_QUERY", "SELECT * FROM properties_test")
        else:
            query = os.environ.get("TRAIN_QUERY", "SELECT * FROM properties_train")

        logging.info(f"Running query: {query}")
        return pd.read_sql(query, engine)

    else:
        raise ValueError(f"Unsupported data source: {source}")


# Setup data cleaning rules
def clean_data(df):
    df = df.drop_duplicates()
    df = df[df["net_area"] > 10]
    df = df[df["net_usable_area"] > 10]
    df = df[(df["n_rooms"] > 0) & (df["n_rooms"] <= 10)]
    df = df[(df["n_bathroom"] >= 0) & (df["n_bathroom"] <= 10)]
    df = df[df["price"] >= 1000]
    df = df[df["net_area"] < 10000]
    df = df[df["net_usable_area"] < 10000]
    price_cap = df["price"].quantile(0.99)
    df = df[df["price"] <= price_cap]
    df = df[(df["latitude"].between(-90, 90)) & (df["latitude"] != 0)]
    df = df[(df["longitude"].between(-180, 180)) & (df["longitude"] != 0)]
    return df