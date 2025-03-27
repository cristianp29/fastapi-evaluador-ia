import requests
from config import API_KEY
from utils.text_processing import normalize_city_name  # Importamos la función correcta

def get_geocode(city_name):
    """Obtiene las coordenadas de una ciudad usando OpenCage Geocoder."""
    
    corrected_name = normalize_city_name(city_name)  # Usamos la función correcta
    print("Corrected Name:", corrected_name)
    
    url = f"https://api.opencagedata.com/geocode/v1/json?q={corrected_name}&key={API_KEY}&language=es"
    response = requests.get(url)
    data = response.json()

    if data["results"]:
        result = data["results"][0]
        lat = result["geometry"]["lat"]
        lng = result["geometry"]["lng"]
        return {
            "corrected_name": corrected_name,
            "latitude": lat,
            "longitude": lng
        }

    return {
        "corrected_name": corrected_name,
        "latitude": None,
        "longitude": None
    }
