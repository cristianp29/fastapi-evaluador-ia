from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geocoder import correct_city_name, get_geocode  # Importamos las funciones

app = FastAPI()

class CityRequest(BaseModel):
    cities: list[str]

@app.post("/geocode/")
def geocode_cities(request: CityRequest):
    """
    Endpoint que recibe una lista de ciudades y devuelve sus coordenadas corregidas.
    """
    city_data = []

    for city in request.cities:
        corrected_city = correct_city_name(city)  # Corrige la ciudad
        geo_info = get_geocode(corrected_city)  # Obtiene coordenadas

        city_data.append({
            "name": city,
            "corrected_name": corrected_city,
            "latitude": geo_info["latitude"] if geo_info else None,
            "longitude": geo_info["longitude"] if geo_info else None
        })

    if not city_data:
        raise HTTPException(status_code=404, detail="No se encontraron ubicaciones válidas.")

    return {"cities": city_data}

