import requests
from rapidfuzz import process
from utils import normalize_text  # Importamos la función de utils.py

# 📍 Lista de ciudades en Colombia
KNOWN_CITIES = [
    "Bogotá, Cundinamarca", "Medellín, Antioquia", "Barranquilla, Atlántico",
    "Cartagena, Bolívar", "Bucaramanga, Santander", "Ocaña, Norte de Santander",
    "Toca, Boyacá", "Jesús María, Santander", "Galapa, Atlántico"
]

API_KEY = "88159997ae24418fb00d49e3c4d41cae"  # Reemplazar con una variable de entorno

def correct_city_name(city_name: str) -> str:
    """
    Corrige nombres de ciudades eliminando errores de codificación y usando coincidencias difusas.
    """
    try:
        city_name = city_name.encode("latin1").decode("utf-8")  # Corrige caracteres mal codificados
    except UnicodeEncodeError:
        pass  # Si falla, continúa con el texto original

    # Normalizar la ciudad ingresada
    normalized_city = normalize_text(city_name)

    # 🔹 Primero verifica si la ciudad ya está en la lista (búsqueda exacta)
    for original_city in KNOWN_CITIES:
        if normalize_text(original_city) == normalized_city:
            return original_city  # Devuelve la ciudad exacta

    # 🔹 Si no se encontró, usar fuzzy matching con un umbral más alto
    best_match = process.extractOne(normalized_city, [normalize_text(c) for c in KNOWN_CITIES], score_cutoff=90)

    if best_match:
        for original_city in KNOWN_CITIES:
            if normalize_text(original_city) == best_match[0]:
                return original_city  # Devuelve la versión correcta con acentos

    return city_name  # Si no hay coincidencia, devuelve el original sin modificar



def get_geocode(city: str):
    """
    Obtiene coordenadas geográficas desde la API de OpenCage.
    """
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={API_KEY}"
    response = requests.get(url).json()

    if response.get("results"):
        best_result = response["results"][0]
        return {
            "latitude": best_result["geometry"]["lat"],
            "longitude": best_result["geometry"]["lng"]
        }
    return None

