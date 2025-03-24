from transformers import pipeline
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BERTQuestionAnswering:
    def __init__(self, model_name=None):
        """
        Inicializa el modelo BERT para responder preguntas
        
        Args:
            model_name: Nombre del modelo pre-entrenado a usar (opcional)
        """
        self.model_name = model_name or "distilbert-base-cased-distilled-squad"  # Modelo por defecto
        self.pipeline = None
        self.is_loaded = False
        self.load_time = None
        self.total_queries = 0
        self.load_model()
    
    def load_model(self):
        """Carga el modelo BERT para question-answering"""
        try:
            start_time = time.time()
            logger.info(f"Cargando modelo BERT: {self.model_name}")
            
            # Inicializar el pipeline de question-answering con el modelo especificado
            self.pipeline = pipeline("question-answering", model=self.model_name)
            
            self.load_time = time.time() - start_time
            self.is_loaded = True
            
            logger.info(f"Modelo cargado en {self.load_time:.2f} segundos")
            return True
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {str(e)}")
            self.is_loaded = False
            return False
    
    def answer_question(self, question, context):
        """
        Responde una pregunta basada en el contexto proporcionado
        
        Args:
            question: La pregunta a responder
            context: El texto de contexto donde buscar la respuesta
            
        Returns:
            Un diccionario con la respuesta, puntuación de confianza y tiempo de procesamiento
        """
        if not self.is_loaded or not self.pipeline:
            return {
                "error": "El modelo no está cargado correctamente",
                "success": False
            }
        
        # Validar entradas
        if not question or not context:
            return {
                "error": "La pregunta y el contexto son obligatorios",
                "success": False
            }
        
        try:
            # Medir tiempo de procesamiento
            start_time = time.time()
            
            # Obtener respuesta del modelo
            result = self.pipeline(question=question, context=context)
            
            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time
            
            # Incrementar contador de consultas
            self.total_queries += 1
            
            # Preparar y devolver resultado
            return {
                "answer": result["answer"],
                "confidence": result["score"],
                "start": result["start"],
                "end": result["end"],
                "process_time": process_time,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error al procesar la pregunta: {str(e)}")
            return {
                "error": f"Error al procesar la pregunta: {str(e)}",
                "success": False
            }
    
    def get_model_info(self):
        """Devuelve información sobre el modelo"""
        return {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "load_time": self.load_time,
            "total_queries": self.total_queries,
            "type": "BERT Question-Answering"
        }

    def extract_highlights(self, context, answer, window=20):
        """
        Extrae un fragmento destacado del contexto alrededor de la respuesta
        
        Args:
            context: El texto completo de contexto
            answer: La respuesta encontrada
            window: Número de caracteres antes y después de la respuesta a incluir
            
        Returns:
            Texto destacado con la respuesta marcada
        """
        if not answer or answer not in context:
            return context
            
        # Encontrar la posición de la respuesta en el contexto
        start_pos = context.find(answer)
        if start_pos == -1:
            return context
            
        # Calcular la ventana de contexto
        highlight_start = max(0, start_pos - window)
        highlight_end = min(len(context), start_pos + len(answer) + window)
        
        # Extraer el fragmento
        before = context[highlight_start:start_pos]
        after = context[start_pos + len(answer):highlight_end]
        
        # Si el fragmento no empieza al inicio del contexto, añadir "..."
        if highlight_start > 0:
            before = "..." + before
            
        # Si el fragmento no termina al final del contexto, añadir "..."
        if highlight_end < len(context):
            after = after + "..."
            
        return f"{before}[{answer}]{after}"

# Si se ejecuta como script principal
if __name__ == "__main__":
    print("\n=== Demo de BERT Question-Answering ===")
    
    # Crear instancia del modelo
    qa = BERTQuestionAnswering()
    
    # Texto de ejemplo
    context = """
    The Solar System is the gravitationally bound system of the Sun and the objects that orbit it,
    either directly or indirectly. Of the objects that orbit the Sun directly, the largest are the eight planets,
    with the remainder being smaller objects, the dwarf planets and small Solar System bodies.
    The Solar System formed 4.6 billion years ago from the gravitational collapse of a giant interstellar molecular cloud.
    """
    
    # Ejemplo inicial
    question = "How old is the Solar System?"
    result = qa.answer_question(question, context)
    
    if result["success"]:
        print(f"\nPregunta: {question}")
        print(f"Respuesta: {result['answer']}")
        print(f"Confianza: {result['confidence']:.4f}")
        print(f"Contexto destacado: {qa.extract_highlights(context, result['answer'])}")
        print(f"Tiempo de procesamiento: {result['process_time']:.2f} segundos")
    else:
        print(f"Error: {result['error']}")
    
    # Modo interactivo
    print("\n--- Modo Interactivo ---")
    print("Escribe 'salir' en cualquier momento para terminar.")
    
    user_context = input("\nPega tu texto de contexto (o presiona Enter para usar el ejemplo):\n").strip()
    if not user_context:
        user_context = context
        print("Usando el contexto de ejemplo.")
    
    while True:
        user_question = input("\nEscribe tu pregunta: ").strip()
        if user_question.lower() in ["salir", "exit", "quit"]:
            break
            
        if not user_question:
            print("Por favor, escribe una pregunta válida.")
            continue
            
        # Procesar la pregunta
        result = qa.answer_question(user_question, user_context)
        
        if result["success"]:
            print(f"\nRespuesta: {result['answer']}")
            print(f"Confianza: {result['confidence']:.4f}")
            print(f"Contexto: {qa.extract_highlights(user_context, result['answer'])}")
        else:
            print(f"Error: {result['error']}")
    
    print("\n¡Gracias por usar BERT Question-Answering!") 