from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from services.geocoder import get_geocode  # Asegúrate de que esta función está bien implementada

# Modelo para recibir las ciudades
class CityRequest(BaseModel):
    cities: list[str]  # Lista de nombres de ciudades recibidas en JSON

# Use lifespan for startup and shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI application...")
    yield  # App runs aquí
    print("Shutting down FastAPI application...")

# Inicializa FastAPI con lifespan
app = FastAPI(lifespan=lifespan)

@app.post("/cities/")
async def get_cities(city_request: CityRequest):
    results = []
    
    for city in city_request.cities:
        geo_data = get_geocode(city)  # Busca coordenadas en el geocoder
        city_data = {
            "name": city,
            "corrected_name": geo_data.get("corrected_name", city),
            "latitude": geo_data.get("latitude"),
            "longitude": geo_data.get("longitude")
        }
        results.append(city_data)
    
    return {"cities": results}
