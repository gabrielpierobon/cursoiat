import os
import json
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import time

# Importar la clase QwenChatModel
from qwen_model import QwenChatModel

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar la aplicación Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Habilitar CORS para permitir peticiones desde orígenes diferentes

# Configuración predeterminada
DEFAULT_SYSTEM_PROMPT = "Eres un asistente de IA útil, respetuoso y sincero. Responde siempre de la mejor manera posible y con información precisa."

# Variable global para el modelo (se inicializará al arrancar)
qwen_chat = None

def initialize_model():
    """Inicializa el modelo Qwen"""
    global qwen_chat
    logger.info("Inicializando modelo Qwen Chat...")
    qwen_chat = QwenChatModel()
    
    # Verificar si el modelo se ha cargado correctamente
    model_info = qwen_chat.get_model_info()
    if model_info.get("is_loaded", False):
        logger.info("Modelo inicializado correctamente.")
        return True
    else:
        logger.error("No se pudo cargar el modelo Qwen.")
        return False

# Rutas de la API
@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para interacción de chat con el modelo"""
    global qwen_chat
    
    # Verificar que el modelo está cargado
    if not qwen_chat or not qwen_chat.is_loaded:
        return jsonify({
            "error": "El modelo Qwen no está cargado correctamente.",
            "success": False
        }), 500
        
    # Obtener parámetros de la solicitud
    data = request.json
    messages = data.get('messages', [])
    system_prompt = data.get('system_prompt', DEFAULT_SYSTEM_PROMPT)
    max_tokens = int(data.get('max_tokens', 512))
    temperature = float(data.get('temperature', 0.7))
    top_p = float(data.get('top_p', 0.9))
    
    # Validar parámetros
    if not messages:
        return jsonify({
            "error": "Se requiere al menos un mensaje.",
            "success": False
        }), 400
    
    # Asegurarse de que el primer mensaje sea del sistema
    if not any(msg.get("role") == "system" for msg in messages):
        messages = [{"role": "system", "content": system_prompt}] + messages
    
    # Interactuar con el modelo
    try:
        start_time = time.time()
        
        result = qwen_chat.generate_response(
            messages=messages,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        
        # Añadir tiempo total (incluyendo proceso API)
        result["total_time"] = time.time() - start_time
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error al procesar la solicitud: {str(e)}")
        return jsonify({
            "error": f"Error al procesar la solicitud: {str(e)}",
            "success": False
        }), 500

@app.route('/api/model_info', methods=['GET'])
def get_model_info():
    """Endpoint para obtener información sobre el modelo cargado"""
    global qwen_chat
    
    if not qwen_chat:
        return jsonify({
            "error": "Modelo no inicializado", 
            "status": "Error",
            "model_name": "Qwen2-7B-Instruct",
            "is_loaded": False
        }), 500
        
    # Obtener información del modelo
    model_info = qwen_chat.get_model_info()
    return jsonify({
        "model_name": model_info.get("model_name", "Qwen2-7B-Instruct"),
        "status": "Cargado" if model_info.get("is_loaded", False) else "No cargado",
        "version": model_info.get("version", "7B"),
        "parameters": model_info.get("parameters", "7.6B"),
        "context_length": model_info.get("context_length", 131072),
        "device": model_info.get("device", "CPU"),
        "total_queries": model_info.get("total_queries", 0)
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
        logger.error("No se pudo inicializar el modelo Qwen.")
        logger.error("Por favor, asegúrese de que las dependencias están instaladas correctamente.") 