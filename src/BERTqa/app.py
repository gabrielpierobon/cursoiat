import os
import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import time
import logging

# Importar la clase BERTQuestionAnswering
from bert_model import BERTQuestionAnswering

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar la aplicación Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Habilitar CORS para permitir peticiones desde orígenes diferentes

# Configuración de ejemplos predefinidos
DEFAULT_EXAMPLES = [
    {
        "title": "Sistema Solar",
        "context": "The Solar System is the gravitationally bound system of the Sun and the objects that orbit it, either directly or indirectly. Of the objects that orbit the Sun directly, the largest are the eight planets, with the remainder being smaller objects, the dwarf planets and small Solar System bodies. The Solar System formed 4.6 billion years ago from the gravitational collapse of a giant interstellar molecular cloud.",
        "questions": ["How old is the Solar System?", "What orbits the Sun?", "How many planets are there?"]
    },
    {
        "title": "Inteligencia Artificial",
        "context": "Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of humans or animals. It is a field of study in computer science that develops and studies intelligent machines. Such machines may be called AI systems. AI may be said to be achieved by any system if it performs functions that would typically require human intelligence, such as visual perception, speech recognition, decision-making, and translating between languages.",
        "questions": ["What is AI?", "What functions can AI systems perform?", "Which field studies AI?"]
    },
    {
        "title": "Cambio Climático",
        "context": "Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, such as through variations in the solar cycle. But since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas, which produces heat-trapping gases. The consequences of climate change now include, among others, intense droughts, water scarcity, severe fires, rising sea levels, flooding, melting polar ice, catastrophic storms and declining biodiversity.",
        "questions": ["What causes climate change?", "When did human activities start affecting climate?", "What are the consequences of climate change?"]
    }
]

# Variable global para el modelo (se inicializará al arrancar)
bert_qa = None

def initialize_model():
    """Inicializa el modelo BERT QA"""
    global bert_qa
    logger.info("Inicializando modelo BERT Question-Answering...")
    bert_qa = BERTQuestionAnswering()
    
    # Verificar si el modelo se ha cargado correctamente
    model_info = bert_qa.get_model_info()
    if model_info.get("is_loaded", False):
        logger.info("Modelo inicializado correctamente.")
        return True
    else:
        logger.error("No se pudo cargar el modelo BERT.")
        return False

# Rutas de la API
@app.route('/api/answer', methods=['POST'])
def answer_question():
    """Endpoint para responder preguntas basadas en contexto"""
    global bert_qa
    
    # Verificar que el modelo está cargado
    if not bert_qa or not bert_qa.is_loaded:
        return jsonify({
            "error": "El modelo BERT no está cargado correctamente.",
            "success": False
        }), 500
        
    # Obtener parámetros de la solicitud
    data = request.json
    question = data.get('question', '')
    context = data.get('context', '')
    
    # Validar parámetros
    if not question or not context:
        return jsonify({
            "error": "Se requieren tanto la pregunta como el contexto.",
            "success": False
        }), 400
    
    # Limitar tamaño del contexto para evitar abusos o problemas
    if len(context) > 10000:  # Limitar a 10k caracteres
        context = context[:10000]
        logger.warning("Contexto truncado a 10000 caracteres")
    
    # Procesar la pregunta
    try:
        start_time = time.time()
        result = bert_qa.answer_question(question, context)
        
        # Si fue exitoso, añadir destacado
        if result.get("success"):
            result["highlight"] = bert_qa.extract_highlights(
                context, 
                result["answer"],
                window=100  # Caracteres antes/después de la respuesta
            )
        
        # Convertir campos para compatibilidad con el cliente
        if "confidence" in result:
            result["score"] = result.pop("confidence")
            
        # Devolver tiempo total
        result["time"] = time.time() - start_time
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error al procesar la solicitud: {str(e)}")
        return jsonify({
            "error": f"Error al procesar la solicitud: {str(e)}",
            "success": False
        }), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Endpoint para obtener ejemplos predefinidos"""
    return jsonify(DEFAULT_EXAMPLES)

@app.route('/api/model_info', methods=['GET'])
def get_model_info():
    """Endpoint para obtener información sobre el modelo cargado"""
    global bert_qa
    
    if not bert_qa:
        return jsonify({"error": "Modelo no inicializado", "status": "Error"}), 500
        
    # Obtener información del modelo y formatear respuesta según lo esperado por el cliente
    model_info = bert_qa.get_model_info()
    return jsonify({
        "model_name": model_info.get("model_name", "desconocido"),
        "status": "Cargado" if model_info.get("is_loaded", False) else "No cargado",
        "version": model_info.get("version", "N/A")
    })

# Rutas para la interfaz web
@app.route('/')
def index():
    """Página principal de la aplicación"""
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Sirve archivos estáticos (CSS, JS, imágenes)"""
    return send_from_directory('static', path)

# Inicialización y punto de entrada principal
if __name__ == '__main__':
    # Intentar inicializar el modelo al arrancar
    model_loaded = initialize_model()
    
    if model_loaded:
        logger.info("Iniciando servidor web en http://localhost:5000")
        # Ejecutar la aplicación Flask
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("No se pudo inicializar el modelo BERT.")
        logger.error("Por favor, asegúrese de que las dependencias están instaladas correctamente.")