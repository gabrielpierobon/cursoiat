import tensorflow as tf
import numpy as np
import re
import json
import os
import sys

class HarryPotterLSTM:
    def __init__(self, model_path=None, vocab_path=None):
        """
        Inicializa el modelo LSTM para generar texto estilo Harry Potter
        
        Args:
            model_path: Ruta al modelo guardado en formato .keras
            vocab_path: Ruta al vocabulario guardado en formato JSON
        """
        self.model = None
        self.token2idx = None
        self.idx2token = None
        
        # Si se proporcionan rutas, cargar el modelo y vocabulario
        if model_path and vocab_path and os.path.exists(model_path) and os.path.exists(vocab_path):
            self.load_model(model_path)
            self.load_vocabulary(vocab_path)
        else:
            print("ADVERTENCIA: Modelo o vocabulario no encontrados. Use load_model() y load_vocabulary() para cargarlos.")

    def load_model(self, model_path):
        """Carga el modelo LSTM desde un archivo"""
        try:
            print(f"Cargando modelo desde: {model_path}")
            self.model = tf.keras.models.load_model(model_path)
            print("Modelo cargado correctamente")
            return True
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return False

    def load_vocabulary(self, vocab_path):
        """Carga el vocabulario desde un archivo JSON"""
        try:
            print(f"Cargando vocabulario desde: {vocab_path}")
            with open(vocab_path, 'r', encoding='utf-8') as f:
                vocab_data = json.load(f)
            
            self.token2idx = vocab_data['token2idx']
            # Convertir claves de string a int para idx2token
            self.idx2token = {int(k): v for k, v in vocab_data['idx2token'].items()}
            
            print(f"Vocabulario cargado con {len(self.token2idx)} tokens")
            return True
        except Exception as e:
            print(f"Error al cargar el vocabulario: {e}")
            return False

    def generate_text(self, prompt, num_tokens=100, temperature=0.7):
        """
        Genera texto basado en un prompt inicial
        
        Args:
            prompt: Texto inicial para comenzar la generación
            num_tokens: Número de tokens (palabras) a generar
            temperature: Controla la aleatoriedad (valores más altos = más aleatorio)
            
        Returns:
            Texto generado incluyendo el prompt
        """
        if not self.model or not self.token2idx or not self.idx2token:
            return "Error: Modelo o vocabulario no cargados"
        
        # Procesar el texto inicial
        prompt = re.sub(r'([.,!¡?¿;:()[\]{}«»""—-])', r' \1 ', prompt)
        start_tokens = prompt.split()
        
        # Convertir tokens iniciales a índices
        input_tokens = []
        for token in start_tokens:
            if token in self.token2idx:
                input_tokens.append(self.token2idx[token])
            else:
                input_tokens.append(self.token2idx.get('<UNK>', 0))  # Token desconocido o 0
        
        # Preparar input para el modelo
        input_ids = tf.expand_dims(input_tokens, 0)
        
        # Lista para tokens generados
        generated_tokens = list(start_tokens)
        
        # Generar texto
        for _ in range(num_tokens):
            # Predecir el siguiente token
            predictions = self.model(input_ids)
            
            # Tomar la última predicción y aplicar temperatura
            predictions = predictions[:, -1, :] / temperature
            
            # Muestrear el siguiente token
            predicted_id = tf.random.categorical(predictions, num_samples=1)[0, 0].numpy()
            
            # Agregar el token predicho al resultado
            generated_tokens.append(self.idx2token.get(predicted_id, "<UNK>"))
            
            # Actualizar entrada con el nuevo token predicho
            input_ids = tf.concat([input_ids, tf.expand_dims([predicted_id], 0)], axis=1)
        
        # Convertir tokens a texto
        generated_text = ' '.join(generated_tokens)
        
        # Limpiar espacios antes y después de signos de puntuación
        generated_text = re.sub(r' ([.,!¡?¿;:()[\]{}«»""—-])', r'\1', generated_text)
        generated_text = re.sub(r'([¿¡]) ', r'\1', generated_text)
        
        return generated_text

    def model_info(self):
        """Devuelve información sobre el modelo"""
        if self.model:
            return {
                "type": "LSTM",
                "vocabulary_size": len(self.token2idx) if self.token2idx else 0,
                "is_loaded": self.model is not None and self.token2idx is not None
            }
        else:
            return {"error": "Modelo no cargado"}

# Si se ejecuta como script principal, ofrecer modo interactivo
if __name__ == "__main__":
    # Rutas por defecto (ajustar según la ubicación real de los archivos)
    default_model_path = os.path.join(os.path.dirname(__file__), "models", "final_token_model_spanish.keras")
    default_vocab_path = os.path.join(os.path.dirname(__file__), "models", "token_vocabulary.json")
    
    # Crear directorio para modelos si no existe
    os.makedirs(os.path.join(os.path.dirname(__file__), "models"), exist_ok=True)
    
    # Si los archivos no existen, imprimir un mensaje
    if not os.path.exists(default_model_path) or not os.path.exists(default_vocab_path):
        print(f"AVISO: Archivos de modelo no encontrados en la ruta por defecto.")
        print(f"Se esperaban archivos en:")
        print(f"  - {default_model_path}")
        print(f"  - {default_vocab_path}")
        print("Por favor, coloque los archivos del modelo en esta ubicación o especifique rutas personalizadas.")
        
    # Inicializar modelo
    lstm = HarryPotterLSTM(default_model_path, default_vocab_path)
    
    # Iniciar modo interactivo
    print("\n=== Generador de Texto Estilo Harry Potter ===")
    print("(Escriba 'salir' para terminar)")
    
    while True:
        prompt = input("\nIngrese texto inicial: ")
        if prompt.lower() in ['salir', 'exit', 'quit']:
            break
            
        try:
            length = int(input("Número de tokens a generar (por defecto 100): ") or "100")
        except ValueError:
            length = 100
            
        try:
            temp = float(input("Temperatura (0.1-2.0, por defecto 0.7): ") or "0.7")
            temp = max(0.1, min(2.0, temp))  # Limitar a rango razonable
        except ValueError:
            temp = 0.7
            
        # Generar y mostrar texto
        print("\n--- TEXTO GENERADO ---")
        generated_text = lstm.generate_text(prompt, length, temp)
        print(generated_text)
        print("---------------------") 