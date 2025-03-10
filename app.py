from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import ollama
import re

app = FastAPI()
@app.get("/")
def home():
    return {"message": "API para evaluación de exámenes en ejecución"}

# Cargar preguntas y respuestas correctas desde un archivo JSON
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

questions_data = load_questions()

# Modelo de datos para la evaluación de exámenes
class Exam(BaseModel):
    student_id: str
    answers: dict  # Diccionario con ID de pregunta como clave y respuesta del estudiante como valor

def evaluate_answer(student_answer, correct_answer):
    messages = [
        {"role": "system", "content": "Eres un asistente de evaluación académica que califica respuestas de estudiantes en una escala del 0 al 5."},
        {"role": "user", "content": f"""
        Evalúa la siguiente respuesta del estudiante y compara con la correcta:
        
        Pregunta: {correct_answer['question']}
        Respuesta del estudiante: {student_answer}
        Respuesta correcta: {correct_answer['answer']}
        
        Debes:
        - Asignar una calificación de 0 a 5 según la precisión.
        - Explicar en máximo 30 palabras por qué se otorga la calificación.
        - Responder solo en español.
        - En la respuesta coloca primero la calificaciion y luego el feedback: Ejemplo: Calificacion: 1. La respuesta no es exacta ya que no responde a la pregunta.
        - Si la respuesta es incorrecta, la calificacion es 0.
        """}
    ]

    response = ollama.chat(model="mistral", messages=messages)
    
    if "message" in response and "content" in response["message"]:
        return response["message"]["content"]
    else:
        return "Error en la respuesta de la IA."

@app.post("/evaluate")
def evaluate_exam(exam: Exam):
    results = []
    total_score = 0
    max_score = len(exam.answers) * 5

    for question_id, student_answer in exam.answers.items():
        correct_answer = questions_data.get(question_id)
        if not correct_answer:
            continue  # Ignorar si la pregunta no está en la base de datos

        evaluation = evaluate_answer(student_answer, correct_answer)
        print(evaluation)

        # 🔹 Expresión regular para extraer el número de calificación
        match = re.search(r"Calificación:\s*(\d+)", evaluation)
        score = int(match.group(1)) if match else 0  # Si no encuentra, asigna 0

        total_score += score  # 🔹 Ahora `score` siempre tiene un valor válido

        results.append({
            "question": correct_answer["question"],
            "student_answer": student_answer,
            "score": score,
            "feedback": evaluation
        })

    final_grade = round((total_score / max_score) * 5, 2)

    return {
        "student_id": exam.student_id,
        "final_grade": final_grade,
        "results": results,
    }