import os
import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import time

# Importar la clase del modelo LSTM
from lstm_model import HarryPotterLSTM

# Inicializar la aplicación Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Habilitar CORS para permitir peticiones desde orígenes diferentes

# Configuración de las rutas a los archivos del modelo
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "final_token_model_spanish.keras")
VOCAB_PATH = os.path.join(MODEL_DIR, "token_vocabulary.json")

# Asegurarse de que el directorio de modelos existe
os.makedirs(MODEL_DIR, exist_ok=True)

# Variable global para el modelo (se inicializará al arrancar)
lstm_model = None

def initialize_model():
    """Inicializa el modelo LSTM"""
    global lstm_model
    print("Inicializando modelo LSTM...")
    lstm_model = HarryPotterLSTM(MODEL_PATH, VOCAB_PATH)
    
    # Verificar si el modelo se ha cargado correctamente
    model_info = lstm_model.model_info()
    if model_info.get("is_loaded", False):
        print("Modelo inicializado correctamente.")
        return True
    else:
        print("ERROR: No se pudo cargar el modelo o vocabulario.")
        print(f"Verifique que los archivos existen en:")
        print(f"  - {MODEL_PATH}")
        print(f"  - {VOCAB_PATH}")
        return False

# Rutas de la API
@app.route('/api/generate', methods=['POST'])
def generate_text():
    """Endpoint para generar texto a partir de un prompt"""
    global lstm_model
    
    # Verificar que el modelo está cargado
    if not lstm_model or not lstm_model.model:
        return jsonify({
            "error": "El modelo no está cargado correctamente. Por favor, verifique los archivos del modelo."
        }), 500
        
    # Obtener parámetros de la solicitud
    data = request.json
    prompt = data.get('prompt', '')
    num_tokens = int(data.get('num_tokens', 100))
    temperature = float(data.get('temperature', 0.7))
    
    # Validar parámetros
    if not prompt:
        return jsonify({"error": "Se requiere un prompt inicial"}), 400
    
    # Limitar valores para evitar abusos
    num_tokens = min(300, max(10, num_tokens))
    temperature = min(2.0, max(0.1, temperature))
    
    # Medir tiempo de generación
    start_time = time.time()
    
    # Generar texto
    try:
        generated_text = lstm_model.generate_text(prompt, num_tokens, temperature)
        generation_time = time.time() - start_time
        
        # Devolver respuesta
        return jsonify({
            "generated_text": generated_text,
            "prompt": prompt,
            "tokens_generated": num_tokens,
            "temperature": temperature,
            "generation_time_seconds": generation_time
        })
    except Exception as e:
        return jsonify({
            "error": f"Error al generar texto: {str(e)}"
        }), 500

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Endpoint para obtener información sobre el modelo cargado"""
    global lstm_model
    
    if not lstm_model:
        return jsonify({"error": "Modelo no inicializado"}), 500
        
    # Obtener y devolver información del modelo
    return jsonify(lstm_model.model_info())

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
        print("Iniciando servidor web en http://localhost:5000")
        # Ejecutar la aplicación Flask
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("ERROR: No se pudo inicializar el modelo LSTM.")
        print("Por favor, asegúrese de que los archivos del modelo están en la ubicación correcta.") 