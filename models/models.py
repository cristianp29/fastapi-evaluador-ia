from pydantic import BaseModel
from typing import List, Optional

class CityRequest(BaseModel):
    cities: List[str]

class CityResponse(BaseModel):
    name: str
    corrected_name: str
    latitude: Optional[float]
    longitude: Optional[float]

class GeocodeResponse(BaseModel):
    cities: List[CityResponse]
