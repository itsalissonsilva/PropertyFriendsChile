from pydantic import BaseModel

# Schema validation used in predict endpoint
class PropertyInput(BaseModel):
    type: str
    sector: str
    net_usable_area: float
    net_area: float
    n_rooms: int
    n_bathroom: int
    latitude: float
    longitude: float

    class Config:
        json_schema_extra = {
            "example": {
                "type": "house",
                "sector": "Providencia",
                "net_usable_area": 85.0,
                "net_area": 100.0,
                "n_rooms": 3,
                "n_bathroom": 2,
                "latitude": -33.4372,
                "longitude": -70.6506
            }
        }

class PredictionOutput(BaseModel):
    predicted_price: float