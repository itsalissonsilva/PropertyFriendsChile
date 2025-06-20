import logging
from fastapi import HTTPException
from app.config import API_KEY

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/app.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_request(data):
    logger.info(f"Request received: {data}")

def validate_api_key(x_api_key):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")