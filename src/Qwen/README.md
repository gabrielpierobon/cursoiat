# Qwen Chat

Una interfaz web tipo ChatGPT que utiliza el modelo Qwen2-1.5B-Instruct para proporcionar respuestas conversacionales.

## Características

- Interfaz de usuario moderna similar a ChatGPT
- Modelo Qwen2-1.5B-Instruct por defecto (ligero, funciona en la mayoría de los equipos)
- Soporte para conversaciones múltiples
- Almacenamiento local de historial de chats
- Configuración de parámetros (temperatura, tokens máximos, prompt del sistema)
- Diseño responsive para móviles y escritorio
- Sistema automático de respaldo a modelo más pequeño si no hay memoria suficiente

## Requisitos

- Python 3.8 o superior
- CUDA (opcional, pero recomendado para mejor rendimiento)
- Al menos 8GB de RAM para el modelo por defecto (Qwen2-1.5B-Instruct)
- Espacio en disco: aproximadamente 3GB para el modelo por defecto

## Instalación

1. Clona este repositorio o descarga los archivos
2. Crea un entorno virtual:
```
python -m venv venv
```
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instala las dependencias:
```
pip install -r requirements.txt
```

## Uso

### Desarrollo

Ejecuta la aplicación Flask en modo desarrollo:

```
python app.py
```

La interfaz estará disponible en `http://localhost:5000`

### Producción

Para un entorno de producción, se recomienda utilizar Gunicorn (Linux/Mac) o Waitress (Windows):

**Linux/Mac (Gunicorn):**
```
gunicorn -w 1 -b 0.0.0.0:8000 app:app
```

**Windows (Waitress):**
```
waitress-serve --port=8000 app:app
```

> **Nota:** Se recomienda usar solo 1 worker (`-w 1`) debido a que el modelo ocupa bastante memoria.

## Estructura del Proyecto

```
Qwen/
├── app.py                # Servidor Flask y API
├── qwen_model.py         # Wrapper para el modelo Qwen
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
├── static/
│   ├── css/
│   │   └── styles.css    # Estilos de la aplicación
│   └── js/
│       └── main.js       # JavaScript de la aplicación
└── templates/
    └── index.html        # Plantilla HTML principal
```

## API

La aplicación proporciona los siguientes endpoints API:

- **POST /api/chat**: Procesar un mensaje de chat
  - Body: JSON con `messages` (array de objetos con `role` y `content`), `system_prompt`, `temperature`, `max_tokens`
  - Respuesta: JSON con `success`, `response`, `time`, `tokens`

- **GET /api/model_info**: Obtener información sobre el modelo cargado
  - Respuesta: JSON con detalles del modelo (nombre, estado, etc.)

## Personalización

### Cambiar el Modelo

Si deseas utilizar otro modelo Qwen o similar, puedes modificar la variable `model_name` en el constructor de la clase `QwenChatModel` dentro del archivo `qwen_model.py`.

Opciones recomendadas:
- `"Qwen/Qwen2-0.5B-Instruct"`: Modelo muy ligero (~1GB), ideal para equipos con recursos limitados
- `"Qwen/Qwen2-1.5B-Instruct"`: Modelo predeterminado (~3GB), buen equilibrio entre rendimiento y recursos
- `"Qwen/Qwen2-7B-Instruct"`: Modelo más grande (~14GB), requiere 16GB+ de RAM, mejor calidad de respuestas

### Ajustes de Rendimiento

Para máquinas con memoria limitada, puedes considerar:
- Reducir la precisión del modelo en `qwen_model.py` (usar `torch.float16` o incluso `torch.int8`)
- Usar versiones más pequeñas del modelo (por ejemplo, Qwen2-1.5B-Instruct)

## Créditos

Este proyecto utiliza:
- [Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct) de Hugging Face
- [Flask](https://flask.palletsprojects.com/) para el servidor web
- [Transformers](https://huggingface.co/docs/transformers/index) para el manejo del modelo

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo LICENSE para más detalles. 