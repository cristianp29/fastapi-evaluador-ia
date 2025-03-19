import unicodedata

def normalize_text(text: str) -> str:
    """
    Limpia y normaliza el texto eliminando acentos y convirtiendo a minúsculas.
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode("utf-8")
    return text.lower().strip()
