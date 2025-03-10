import ollama

print("Bienvenido al chatbot de evaluación de exámenes. Escribe 'salir' para terminar.")

while True:
    pregunta = input("Tú: ")
    if pregunta.lower() == "salir":
        break
    
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": pregunta}])
    print("IA:", response["message"]["content"])
