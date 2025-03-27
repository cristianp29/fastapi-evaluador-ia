from fastapi import FastAPI, HTTPException
from models.city_request import CityRequest
from services import geocoder

app = FastAPI()

@app.post("/geocode/")
def geocode_cities(request: CityRequest):
    city_data = []

    for city in request.cities:
        corrected_city = geocoder.correct_city_name(city)
        geo_info = geocoder.get_geocode(corrected_city)
        
        city_data.append({
            "name": city,
            "corrected_name": corrected_city,
            "latitude": geo_info["latitude"] if geo_info else None,
            "longitude": geo_info["longitude"] if geo_info else None
        })

    if not city_data:
        raise HTTPException(status_code=404, detail="No se encontraron ubicaciones válidas.")

    return {"cities": city_data}

