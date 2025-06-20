# Property Friends: Real Estate Price Prediction in Chile API

This project delivers a machine learning pipeline and RESTful API for real estate price prediction. It's fully containerized using Docker and orchestrated via Docker Compose.


## How to Run (Production Setup)

### 1. Prerequisites

- Docker + Docker Compose installed
- `train.csv` and `test.csv` files inside the `data/` folder
- Rename `.env.example` to `.env` and configure variables as needed
- Required Python dependencies are listed in `requirements.txt` and automatically installed during the Docker build process

### 2. Build and Run Services

Start by building the services:

```bash
docker compose build
```

Then run the pipeline which includes training and evaluation:

```bash
docker compose up pipeline
```

This command triggers the following services in order:

- `train`: trains and serializes the model to `models/model.pkl`
- `evaluate`: evaluates the trained model on the test data
- `pipeline`: dummy service used to enforce execution order

Once the pipeline finishes you can start the API:

```bash
docker compose up api
```

This will start the FastAPI server at [http://localhost:8000](http://localhost:8000), with interactive documentation available at `/docs`.

## API Usage

### Authentication

All endpoints (except `/`, `/health`) require the `x-api-key` header.

Example:

```bash
curl -X POST http://localhost:8000/predict \
  -H "x-api-key: secret123" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "apartment",
    "sector": "central",
    "net_area": 80,
    "net_usable_area": 75,
    "n_rooms": 3,
    "n_bathroom": 2,
    "latitude": -23.56,
    "longitude": -46.63
  }'
```

### Endpoints

| Method | Endpoint      | Description                 |
|--------|---------------|-----------------------------|
| GET    | `/`           | Root message                |
| GET    | `/health`     | API uptime status           |
| POST   | `/predict`    | Predict property price      |

## Configuration

Use the `.env` file to configure data source and API key:

```env
# API
API_KEY=secret123

# Data source: csv or database
DATA_SOURCE=csv

# For DB mode
DB_CONN_STRING=postgresql://user:pass@host/db
TRAIN_QUERY=SELECT * FROM properties_train
TEST_QUERY=SELECT * FROM properties_test

# Model path
MODEL_PATH=models/model.pkl
```


## Docker Compose Overview

```yaml
services:
  pipeline:
    command: >
      bash -c "python pipeline/train.py &&
               python pipeline/evaluate.py"

  api:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    depends_on:
      - pipeline
```

## Assumptions Made

- Standard data cleaning was applied. Duplicate rows were removed before training. Descriptive statistics were computed for all fields, and outlier detection guided column-specific preprocessing thresholds. Some listings contained formatting errors, such as zero or unusually low prices and unrealistically small areas. These were filtered out during preprocessing. Listings with `net_area` or `net_usable_area` below 10 m² were excluded to avoid misreported entries. The target variable `price` was also filtered to remove values below 1000, assuming these reflect test records or data issues. Latitude and longitude values were assumed valid but constrained to realistic geographic bounds as a safeguard.

- The model selected was `GradientBoostingRegressor` which was compared to a baseline `RandomForestRegressor` and outpeformed it in key metrics (MAE, RMSE, MAPE). Model predictions were rounded to the nearest integer to match the format and resolution of the original dataset. The model hyperparameters were tuned using `GridSearchCV` with 5-fold cross-validation to enhance generalization performance.

- By default, the pipeline assumes data comes from CSV files (`data/train.csv`, `data/test.csv`). A `.env` variable (`DATA_SOURCE`) allows switching to a SQL database if desired.



## Areas for Improvement


- For future experiments the client wishes to perform with different models, especially linear ones, preprocessing the numerical columns using transformations such as `StandardScaler`, `MinMaxScaler`, or `PowerTransformer` is advised to handle skewed distributions and improve performance. Future tuning efforts could also leverage `RandomizedSearchCV` for broader and faster exploration of the hyperparameter space.

- Although `net_area` and `net_usable_area` are highly correlated, both were retained in the solution since in real estate they offer distinct interpretive value (e.g., total area vs. usable living space). Future feature pruning may revisit this decision if model performance suggests otherwise.

- To ensure reproducibility and experiment tracking, incorporating tools like MLflow is highly recommended. Additionally, deploying the solution to a cloud environment such as AWS (e.g., using S3 for data, Lambda functions, or SageMaker for managed ML workflows) is advised to enable scalability and production readiness.

