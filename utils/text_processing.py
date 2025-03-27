import json 
from rapidfuzz import process, fuzz
from opencage.geocoder import OpenCageGeocode

# Clave API de OpenCage
TU_API_KEY = "88159997ae24418fb00d49e3c4d41cae"
geocoder = OpenCageGeocode(TU_API_KEY)

# Lista de ciudades conocidas
KNOWN_CITIES = [
    "Bogotá, Cundinamarca", "Medellín, Antioquia", "Barranquilla, Atlántico",
    "Cartagena, Bolívar", "Bucaramanga, Santander", "Ocaña, Norte de Santander", "Toca, Boyacá",
    "Chinú, Córdoba", "Amagá, Antioquia", "Titiribí, Antioquia", "Venecia, Antioquia",
    "Andes, Antioquia", "Sibaté, Cundinamarca", "Guayabetal, Cundinamarca", "La Ceja, Antioquia",
    "Palmar de Varela, Atlántico", "San Pedro de Urabá, Antioquia", "Maní, Casanare",
    "San José del Guaviare, Guaviare", "Guática, Risaralda", "Talaigua Nuevo, Bolívar",
    "Tocancipá, Cundinamarca", "Vélez, Santander", "Girón, Santander", "San Gil, Santander",
    "Socorro, Santander", "Córdoba, Quindío", "Tilodirán, Casanare", "Sabanagrande, Atlántico",
    "Achí, Bolívar", "Sahagún, Córdoba", "Santa Catalina, Bolívar", "Santiago de Tolú, Sucre",
    "Pensilvania, Caldas", "Moquegua, Moquegua", "Tacna, Tacna", "Ponedera, Atlántico",
    "Florencia, Caquetá", "San Onofre, Sucre", "Los Santos, Santander", "San Juan de Arama, Meta",
    "Obando, Valle del Cauca", "Toro, Valle del Cauca", "Jardín, Antioquia", "Jericó, Antioquia",
    "Turbo, Antioquia", "Apartadó, Antioquia", "Marsella, Risaralda", "Cali, Valle del Cauca",
    "Mesa de Los Santos, Santander", "Arequipa, Caravelí", "Villeta, Cundinamarca",
    "Pivijay, Magdalena", "Ciénaga, Magdalena", "Soplaviento, Bolívar", "Carepa, Antioquia",
    "Giraldo, Antioquia", "Frontino, Antioquia", "Jesús María, Santander", "Guadalajara de Buga, Valle del Cauca",
    "Dibulla, La Guajira", "Chiriguaná, Cesar", "Piedecuesta, Santander", "Galapa, Atlántico",
    "Corozal, Sucre", "Chigorodó, Antioquia", "Caucasia, Antioquia", "Garzón, Huila",
    "Villa de San Diego de Ubaté, Cundinamarca", "Mahates, Bolívar", "Támesis, Antioquia",
    "Quibdó, Chocó", "El Tambo, Cauca", "Floridablanca, Santander", "Sabanas de San Ángel, Magdalena",
    "Barrancabermeja, Santander", "San Vicente de Chucurí, Santander", "Villamaría, Caldas",
    "San Cayetano, Norte de Santander", "Barranca, Lima (Perú)", "Lebrija, Santander",
    "Marinilla, Antioquia", "Mongua, Boyacá", "El Cocuy, Boyacá", "Ayacucho, Ayacucho (Perú)",
    "Puerto Colombia, Atlántico", "Villavicencio, Meta", "San Luis de Sincé, Sucre",
    "Candelaria, Atlántico", "Trujillo, Valle del Cauca", "Puerto López, Meta",
    "San Vicente, Antioquia", "Corregimiento Borrero Ayabe de Dagua, Valle del Cauca",
    "Tibasosa, Boyacá", "Doradal, Antioquia", "Itagüí, Antioquia", "Flandes, Tolima",
    "Rionegro, Antioquia", "Carmen de Apicalá, Tolima", "San Juan de Pasto, Nariño",
    "San Pedro, Valle del Cauca", "Roldanillo, Valle del Cauca", "Armenia, Quindío",
    "Soledad, Atlántico", "Tubará, Atlántico", "Santa Lucía, Atlántico", "Necoclí, Antioquia",
    "San Diego, Cesar", "Belén, Boyacá", "Nunchía, Casanare", "Ginebra, Valle del Cauca",
    "El Cerrito, Valle del Cauca", "Fredonia, Antioquia", "Guaranda, Sucre",
    "Planeta Rica, Córdoba", "Villapinzón, Cundinamarca", "Solita, Caquetá",
    "El Retiro, Antioquia", "Barbosa, Santander", "Uribia, La Guajira", "Valledupar, Cesar",
    "Alcalá, Valle del Cauca", "Pacho, Cundinamarca", "Zetaquira, Boyacá", "Sincelejo, Sucre",
    "Montería, Córdoba", "San Pablo, Bolívar", "Guaduas, Cundinamarca", "Morroa, Sucre",
    "Málaga, Santander", "Huánuco, Perú", "Vichaycoto, Perú", "Cucunubá, Cundinamarca",
    "El Bagre, Antioquia", "San Benito Abad, Sucre", "La Unión, Valle del Cauca",
    "Tuluá, Valle del Cauca", "Barranco de Loba, Bolívar", "Nilo, Cundinamarca",
    "San Pedro de los Milagros, Antioquia", "Campoalegre, Huila", "Albán, Cundinamarca",
    "Calima, Valle del Cauca", "Monterrey, Casanare", "San Juan del Cesar, La Guajira"
]


def normalize_city_name(city_name):
    city_name = city_name.lower().replace("ã¡", "á").replace("ã©", "é").replace("ã­", "í").replace("ã³", "ó").replace("ãº", "ú")

    match = process.extractOne(city_name, KNOWN_CITIES, scorer=fuzz.WRatio, score_cutoff=70)

    if match:
        best_match = match[0]
        return best_match

    return city_name
def get_coordinates(city_name):
    """ Obtiene coordenadas de OpenCage API, intentando con el nombre completo y solo la ciudad. """
    result = geocoder.geocode(city_name)
    
    if not result:
        city_only = city_name.split("-")[0].strip()
        result = geocoder.geocode(city_only)

    if result:
        return result[0]["geometry"]["lat"], result[0]["geometry"]["lng"]
    
    return None, None

def process_cities(city_list):
    """ Procesa la lista de ciudades, normalizándolas y obteniendo coordenadas. """
    processed_data = []
    for city in city_list:
        corrected_name = normalize_city_name(city)
        latitude, longitude = get_coordinates(corrected_name)
        processed_data.append({
            "name": city,
            "corrected_name": corrected_name,
            "latitude": latitude,
            "longitude": longitude
        })
    return {"cities": processed_data}

# Ejemplo de entrada
input_data = {
    "cities": [
        "Toca - Boyacá",
        "Los Santos - Santander",
        "Bucaramanga - Santander",
        "Arequipa - Caraveli",
        "Jesús María - Santander",
        "Galapa - Atlantico",
        "Belén - Boyacá",
        "Baffanquiya - Atlantico",
        "Cartajen - Bolibar"
    ]
}

output_data = process_cities(input_data["cities"])
print(json.dumps(output_data, indent=4, ensure_ascii=False))
