Coordenada Cargo

Este proyecto es una API desarrollada con FastAPI para la corrección y normalización de nombres de ciudades en Colombia, proporcionando coordenadas geográficas.

🚀 Instalación y Configuración

1️⃣ Clonar el repositorio

2️⃣ Crear y activar un entorno virtual

3️⃣ Instalar las dependencias

4️⃣ Descargar modelo de idioma para spaCy (si aplica)

5️⃣ Ejecutar la API

La API estará disponible en: http://127.0.0.1:8000

📂 Estructura del Proyecto

📡 Endpoints

Método

Endpoint

Descripción

GET

/health

Verifica si la API está funcionando

POST

/geocode

Normaliza el nombre de una ciudad y obtiene coordenadas

Ejemplo de solicitud POST /geocode:

Ejemplo de respuesta:

🛠 Tecnologías Utilizadas

FastAPI: Framework rápido para APIs en Python

Uvicorn: Servidor ASGI

spaCy: Procesamiento de lenguaje natural

requests: Peticiones HTTP

Pydantic: Validación de datos

📌 Notas

Si el puerto 8000 ya está en uso, ejecuta Uvicorn en otro puerto:

✅ Pruebas

Ejecutar pruebas unitarias:

📄 Licencia

Este proyecto está bajo la licencia MIT.

