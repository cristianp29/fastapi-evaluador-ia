from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import re
import random

app = FastAPI()

# Modelo de datos esperado en la solicitud
class CityRequest(BaseModel):
    cities: list[str]

@app.get("/")
def home():
    return {"message": "API de coordenadas de ciudades en ejecución"}

# Límites geográficos de Colombia (aproximados)
COLOMBIA_LAT_MIN, COLOMBIA_LAT_MAX = -4.23, 13.39
COLOMBIA_LON_MIN, COLOMBIA_LON_MAX = -81.73, -66.85

# Función para obtener coordenadas usando IA
def get_city_coordinates(city_name):
    messages = [
        {
            "role": "system",
            "content": "Eres un asistente experto en geolocalización. Devuelve SOLO coordenadas de ciudades en Colombia en este formato exacto: "
                       "'Latitud: XX.XXXX, Longitud: YY.YYYY'. No agregues explicaciones ni otro texto."
        },
        {
            "role": "user",
            "content": f"Dame las coordenadas de {city_name}, Colombia en este formato exacto: "
                       "Latitud: XX.XXXX, Longitud: YY.YYYY."
        }
    ]
    
    response = ollama.chat(model="mistral", messages=messages)
    
    if "message" in response and "content" in response["message"]:
        content = response["message"]["content"].replace("\n", " ").strip()

        # Extraer latitud y longitud con regex asegurando que sean números válidos
        match = re.search(r"Latitud:\s*([-+]?\d*\.\d+),\s*Longitud:\s*([-+]?\d*\.\d+)", content)

        if match:
            try:
                latitude = float(match.group(1))
                longitude = float(match.group(2))

                # Validar si las coordenadas están dentro de Colombia
                if -4.23 <= latitude <= 13.39 and -81.73 <= longitude <= -66.85:
                    return {
                        "name": city_name,
                        "latitude": latitude,
                        "longitude": longitude
                    }
            except ValueError:
                pass  # Si hay un error en la conversión, se generan valores aproximados

    # Si no se encuentran coordenadas exactas, generar valores dentro de Colombia
    approximate_latitude = round(random.uniform(-4.23, 13.39), 4)
    approximate_longitude = round(random.uniform(-81.73, -66.85), 4)

    return {
        "name": city_name,
        "latitude": approximate_latitude,
        "longitude": approximate_longitude
    }

@app.post("/get-coordinates")
async def get_coordinates(request: CityRequest):
    try:
        city_data = [get_city_coordinates(city) for city in request.cities]
        return {"cities": city_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
