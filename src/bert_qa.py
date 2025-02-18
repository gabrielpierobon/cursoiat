from transformers import pipeline
import time

def mostrar_intro():
    """Muestra la introducción y documentación del demo"""
    print("\n" + "*" * 78)
    print("*  BERT Question-Answering Demo")
    print("*  Demostración de respuesta a preguntas usando BERT")
    print("*" + "*" * 71)
    
    print("""
Este demo utiliza BERT (Bidirectional Encoder Representations from Transformers) para
responder preguntas sobre un texto dado. El modelo ha sido pre-entrenado en el dataset
SQuAD (Stanford Question Answering Dataset).

Características:
- Utiliza la librería transformers de Hugging Face
- Carga un modelo BERT pre-entrenado para question-answering
- Puede responder preguntas sobre cualquier texto proporcionado
- Proporciona un puntaje de confianza para cada respuesta

El demo funciona en dos partes:
1. Primero verás un ejemplo usando información del Sistema Solar
2. Luego podrás ingresar tu propio texto y hacer preguntas sobre él

Para cada respuesta, el modelo proporcionará:
- La respuesta extraída del texto
- Un puntaje de confianza (entre 0 y 1)

Nota: Este demo usa el modelo BERT por defecto. Para usar otros modelos, modifica:
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
""")
    input("\nPresiona Enter para comenzar el demo...")

def main():
    mostrar_intro()
    
    # Crear el pipeline de question-answering
    print("\nInicializando modelo BERT...")
    qa_pipeline = pipeline("question-answering")
    print("Modelo cargado exitosamente.")
    
    # Contexto de ejemplo
    print("\nEjemplo inicial usando información del Sistema Solar:")
    context = """
    The Solar System is the gravitationally bound system of the Sun and the objects that orbit it, 
    either directly or indirectly. Of the objects that orbit the Sun directly, the largest are the eight planets, 
    with the remainder being smaller objects, the dwarf planets and small Solar System bodies. 
    The Solar System formed 4.6 billion years ago from the gravitational collapse of a giant interstellar molecular cloud.
    """
    print("\nContexto de ejemplo:")
    print(context)
    
    # Ejemplo inicial
    question = "How old is the Solar System?"
    print("\nPregunta de ejemplo:", question)
    print("Procesando...")
    time.sleep(1)
    
    result = qa_pipeline(question=question, context=context)
    print(f"Respuesta: {result['answer']}")
    print(f"Confianza: {result['score']:.4f}")
    
    # Sección interactiva
    print("\n" + "=" * 78)
    print("MODO INTERACTIVO")
    print("=" * 78)
    print("\nAhora puedes probar con tu propio texto.")
    print("Recomendaciones:")
    print("- Usa un texto claro y bien estructurado")
    print("- Las preguntas deben poder responderse con la información del texto")
    print("- El modelo funciona mejor con preguntas directas")
    print("- Escribe 'exit' en cualquier momento para salir")
    
    user_context = input("\nPega tu texto aquí:\n")
    print("\nTexto recibido. Puedes empezar a hacer preguntas.")
    
    while True:
        user_question = input("\nHaz una pregunta (escribe 'exit' para salir): ")
        if user_question.lower() == 'exit':
            print("\nGracias por usar el demo de BERT Question-Answering.")
            break
            
        print("Procesando pregunta...")
        time.sleep(0.5)
        result = qa_pipeline(question=user_question, context=user_context)
        
        print("\nResultados:")
        print(f"Pregunta: {user_question}")
        print(f"Respuesta: {result['answer']}")
        print(f"Confianza: {result['score']:.4f}")
        
        if result['score'] < 0.2:
            print("\nNota: La confianza es baja. Considera reformular la pregunta o verificar si la")
            print("      información necesaria está presente en el texto.")

if __name__ == "__main__":
    main() 