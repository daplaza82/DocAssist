"""
DocAssist Academic - Sistema MVP para análisis de documentos académicos.
Utiliza GPT-3.5 Turbo a través de Azure para procesar documentos y responder preguntas.
"""

from flask import Blueprint, request, jsonify, render_template, current_app
import openai
from PyPDF2 import PdfReader
import io
import time
import random

# Crear el Blueprint
main = Blueprint('main', __name__)

def process_with_mistral(prompt, max_tokens=500, max_retries=3):
    """Procesa texto usando GPT-3.5 Turbo con manejo de límites de velocidad."""
    for attempt in range(max_retries):
        try:
            # Añadir un pequeño retraso aleatorio para evitar límites de velocidad
            time.sleep(random.uniform(1, 3))
            
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente académico experto en analizar documentos y generar resúmenes concisos y precisos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message['content'].strip()
            
        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message:
                if attempt < max_retries - 1:
                    # Esperar 10 segundos antes de reintentar
                    time.sleep(10)
                    continue
            print(f"Error detallado (intento {attempt + 1}): {str(e)}")
            raise Exception(f"Error al procesar el documento (intento {attempt + 1}): {str(e)}")
    
    raise Exception("Se alcanzó el número máximo de intentos")

def extract_text_from_pdf(pdf_file):
    """Extrae texto de un archivo PDF."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error al procesar PDF: {str(e)}")

@main.route('/')
def index():
    """Página principal."""
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze_document():
    """Analiza un documento PDF."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
            
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Solo se aceptan archivos PDF'}), 400

        # Extraer texto del PDF
        text = extract_text_from_pdf(file)
        
        # Dividir el texto en secciones más pequeñas si es necesario
        max_chars = 2000  # Reducido para evitar límites de tokens
        text_for_analysis = text[:max_chars]  # Usar solo la primera parte para el análisis inicial

        # Esperar un momento antes de hacer la primera llamada a la API
        time.sleep(2)

        # Generar resumen
        summary_prompt = f"Genera un resumen ejecutivo conciso del siguiente texto académico. El resumen debe ser de máximo 3 párrafos:\n\n{text_for_analysis}"
        summary = process_with_mistral(summary_prompt, max_tokens=300)

        # Esperar antes de la segunda llamada
        time.sleep(2)

        # Extraer puntos clave
        points_prompt = f"Identifica y lista los 3 puntos más importantes del siguiente texto académico:\n\n{text_for_analysis}"
        key_points = process_with_mistral(points_prompt, max_tokens=200)

        # Guardar documento en Azure Blob
        blob_service_client = current_app.config['BLOB_SERVICE_CLIENT']
        container_name = "documentos"
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
        
        blob_client = container_client.get_blob_client(file.filename)
        file.seek(0)
        blob_client.upload_blob(file, overwrite=True)

        return jsonify({
            'summary': summary,
            'key_points': key_points,
            'text': text_for_analysis,  # Enviamos solo la parte analizada
            'message': 'Documento procesado exitosamente'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/question', methods=['POST'])
def answer_question():
    """Responde preguntas sobre el documento."""
    try:
        data = request.get_json()
        question = data.get('question')
        text = data.get('text')

        if not question or not text:
            return jsonify({'error': 'Pregunta o contexto faltante'}), 400

        prompt = f"""Basado en el siguiente texto académico, responde la pregunta.
        Si la información no está en el texto, indica que no puedes responder.

        Texto: {text[:4000]}

        Pregunta: {question}"""

        answer = process_with_mistral(prompt, max_tokens=300)

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500