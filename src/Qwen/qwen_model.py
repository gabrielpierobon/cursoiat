import time
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QwenChatModel:
    """Clase para gestionar la interacción con el modelo Qwen2-7B-Instruct"""
    
    def __init__(self, model_name=None):
        """
        Inicializa el modelo Qwen
        
        Args:
            model_name: Nombre del modelo pre-entrenado a usar (opcional)
        """
        self.model_name = model_name or "Qwen/Qwen2-1.5B-Instruct"  # Modelo más pequeño por defecto
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.load_time = None
        self.total_queries = 0
        self.load_model()
    
    def load_model(self):
        """Carga el modelo Qwen para generación de texto"""
        try:
            start_time = time.time()
            logger.info(f"Intentando cargar modelo {self.model_name}...")
            
            # Determinar el tipo de datos según la disponibilidad de CUDA
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Cargar el modelo
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=dtype,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            # Cargar el tokenizador
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            self.load_time = time.time() - start_time
            self.is_loaded = True
            logger.info(f"Modelo {self.model_name} cargado correctamente en {self.load_time:.2f} segundos.")
            
        except Exception as e:
            logger.error(f"Error al cargar el modelo {self.model_name}: {str(e)}")
            
            # Si el modelo actual no es ya el más pequeño, intentar con uno más pequeño
            if "Qwen2-0.5B" not in self.model_name:
                fallback_model = "Qwen/Qwen2-0.5B-Instruct"
                logger.info(f"Intentando cargar modelo más pequeño: {fallback_model}")
                try:
                    self.model_name = fallback_model
                    
                    # Cargar el modelo más pequeño
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.model_name,
                        torch_dtype=torch.float32,  # Usar precisión normal para el modelo pequeño
                        device_map="auto" if torch.cuda.is_available() else None,
                        trust_remote_code=True
                    )
                    
                    # Cargar el tokenizador
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model_name,
                        trust_remote_code=True
                    )
                    
                    self.load_time = time.time() - start_time
                    self.is_loaded = True
                    logger.info(f"Modelo de respaldo {fallback_model} cargado correctamente en {self.load_time:.2f} segundos.")
                except Exception as fallback_error:
                    logger.error(f"Error al cargar modelo de respaldo: {str(fallback_error)}")
                    self.is_loaded = False
            else:
                self.is_loaded = False
    
    def generate_response(self, messages, max_new_tokens=512, temperature=0.7, top_p=0.9):
        """
        Genera una respuesta basada en la conversación proporcionada
        
        Args:
            messages: Lista de mensajes en formato ChatML [{"role": "user", "content": "..."}, ...]
            max_new_tokens: Número máximo de tokens a generar
            temperature: Temperatura para muestreo
            top_p: Valor de top-p para muestreo nucleico
            
        Returns:
            dict: Diccionario con la respuesta y metadatos
        """
        if not self.is_loaded:
            return {
                "success": False, 
                "error": "El modelo no está cargado correctamente.",
                "response": None
            }
        
        try:
            start_time = time.time()
            
            # Asegurarse de que hay un mensaje de sistema, o añadir uno predeterminado
            if not any(msg.get("role") == "system" for msg in messages):
                messages = [{"role": "system", "content": "Eres un asistente de IA útil, respetuoso y sincero."}] + messages
            
            # Aplicar la plantilla de chat
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Codificar
            model_inputs = self.tokenizer([text], return_tensors="pt")
            if torch.cuda.is_available():
                model_inputs = model_inputs.to("cuda")
            
            # Generar respuesta
            with torch.no_grad():
                generated_ids = self.model.generate(
                    model_inputs.input_ids,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=temperature > 0,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Extraer solo los tokens generados (no los de entrada)
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]
            
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Actualizar contador y calcular tiempo
            self.total_queries += 1
            process_time = time.time() - start_time
            
            return {
                "success": True,
                "response": response.strip(),
                "time": process_time,
                "tokens": len(generated_ids[0])
            }
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {str(e)}")
            return {
                "success": False,
                "error": f"Error al generar respuesta: {str(e)}",
                "response": None
            }
    
    def get_model_info(self):
        """
        Obtiene información sobre el modelo cargado
        
        Returns:
            dict: Diccionario con información del modelo
        """
        info = {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "load_time": self.load_time,
            "total_queries": self.total_queries,
            "version": "7B",
            "parameters": "7.6B",
            "context_length": 131072,
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        }
        
        return info 