import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener API Key desde las variables de entorno
API_KEY = os.getenv("API_KEY")

# Lista de ciudades conocidas
KNOWN_CITIES = [
    "Bogotá, Cundinamarca", "Medellín, Antioquia", "Barranquilla, Atlántico",
    "Cartagena, Bolívar", "Bucaramanga, Santander", "Ocaña, Norte de Santander"
]
