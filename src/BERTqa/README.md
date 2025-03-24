# BERT-QA: Sistema de Preguntas y Respuestas con BERT

BERT-QA es una aplicación web que utiliza modelos BERT (Bidirectional Encoder Representations from Transformers) para proporcionar respuestas a preguntas basadas en un contexto proporcionado. La aplicación ofrece una interfaz tipo ChatGPT para una experiencia de usuario intuitiva.

## Características

- Interfaz web moderna similar a ChatGPT
- Análisis de contexto mediante el modelo BERT
- Respuestas generadas basadas exclusivamente en el contexto proporcionado
- Resaltado de fragmentos relevantes del texto
- Ejemplos predefinidos para facilitar el uso
- API REST para integración con otros sistemas

## Requisitos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Conexión a internet (para la descarga inicial del modelo BERT)

## Instalación

1. Clona este repositorio o descarga los archivos en tu sistema local
2. Navega al directorio del proyecto
3. Crea un entorno virtual (recomendado):
```
python -m venv venv
```
4. Activa el entorno virtual:
   - En Windows:
   ```
   venv\Scripts\activate
   ```
   - En macOS/Linux:
   ```
   source venv/bin/activate
   ```
5. Instala las dependencias:
```
pip install -r requirements.txt
```

## Uso

### Ejecutar el servidor en desarrollo

```
python app.py
```

El servidor estará disponible en `http://localhost:5000` por defecto.

### Ejecutar en producción

Para entornos de producción, se recomienda utilizar Gunicorn (Linux/macOS) o Waitress (Windows):

Con Gunicorn (Linux/macOS):
```
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Con Waitress (Windows):
```
waitress-serve --port=8000 app:app
```

## Estructura del Proyecto

```
BERTqa/
├── app.py                # Servidor Flask y rutas API
├── bert_model.py         # Implementación del modelo BERT
├── requirements.txt      # Dependencias del proyecto
├── static/               # Archivos estáticos
│   ├── css/              # Hojas de estilo
│   │   └── styles.css    # Estilos de la aplicación
│   └── js/               # JavaScript
│       └── main.js       # Lógica de la interfaz de usuario
└── templates/            # Plantillas HTML
    └── index.html        # Página principal
```

## API REST

La aplicación proporciona una API REST con los siguientes endpoints:

- `POST /api/answer`: Responde a preguntas basadas en un contexto
  - Parámetros (JSON): `context` (texto de contexto), `question` (pregunta)
  - Respuesta: `{'answer': 'respuesta', 'highlight': 'texto resaltado', 'score': confianza, 'time': tiempo_proceso}`

- `GET /api/examples`: Obtiene ejemplos predefinidos
  - Respuesta: Lista de ejemplos con contexto, título y preguntas

- `GET /api/model_info`: Obtiene información sobre el modelo BERT
  - Respuesta: `{'model_name': 'nombre del modelo', 'status': 'estado', 'version': 'versión'}`

## Personalización

### Cambiar el modelo BERT

Para usar un modelo BERT diferente, modifica la constante `MODEL_NAME` en el archivo `bert_model.py`. Asegúrate de que el modelo sea compatible con el procesamiento de preguntas y respuestas.

### Añadir ejemplos

Puedes añadir más ejemplos modificando la lista `EXAMPLES` en el archivo `app.py`. Cada ejemplo debe tener un título, un contexto y una lista de preguntas relacionadas.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Créditos

Este proyecto utiliza el modelo BERT desarrollado por Google Research y la implementación de Hugging Face Transformers. 