import unicodedata
import spacy
import rapidfuzz

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

KNOWN_CITIES = [
    "Bogotá, Cundinamarca", "Medellín, Antioquia", "Barranquilla, Atlántico",
    "Cartagena, Bolívar", "Bucaramanga, Santander", "Ocaña, Norte de Santander"
]

def normalize_text(text: str) -> str:
    """Limpia y normaliza el texto usando spaCy."""
    doc = nlp(text.lower())
    normalized_tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(normalized_tokens)

def correct_city_name(city_name: str) -> str:
    """Corrige y normaliza el nombre de la ciudad."""
    try:
        city_name = city_name.encode("latin1").decode("utf-8")
    except UnicodeEncodeError:
        pass  

    normalized_city = unicodedata.normalize('NFKD', city_name).encode('ascii', 'ignore').decode("utf-8")
    best_match = process.extractOne(normalized_city, KNOWN_CITIES, score_cutoff=80)

    if best_match:
        corrected_name = best_match[0]
        if "," not in corrected_name:
            for city in KNOWN_CITIES:
                if corrected_name in city:
                    corrected_name = city
                    break
        return corrected_name

    return city_name
