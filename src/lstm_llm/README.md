# HarryGPT - Generador de Texto basado en LSTM

Este proyecto demuestra cómo implementar un modelo de lenguaje LSTM (Long Short-Term Memory) para generar texto con estilo de Harry Potter, con una interfaz web similar a ChatGPT.

![HarryGPT Screenshot](https://via.placeholder.com/800x450.png?text=HarryGPT+Screenshot)

## 📋 Descripción

El proyecto incluye:

1. **Modelo LSTM**: Un modelo pre-entrenado con textos de Harry Potter para generar texto similar
2. **API REST**: Un backend con Flask que expone el modelo a través de endpoints API
3. **Interfaz Web**: Una interfaz de usuario estilo ChatGPT para interactuar con el modelo

## 🧠 Cómo funciona el modelo LSTM

Los modelos LSTM (Long Short-Term Memory) son un tipo de red neuronal recurrente (RNN) capaces de aprender dependencias a largo plazo en los datos secuenciales, como texto.

En este ejemplo:
- El modelo ha sido pre-entrenado con textos de Harry Potter
- Utiliza palabras (tokens) como unidades de entrada y salida
- Se puede ajustar la "temperatura" para controlar la creatividad/variabilidad
- Mayor temperatura (>1.0) = más aleatorio y creativo
- Menor temperatura (<1.0) = más predecible y coherente

## 🛠️ Requisitos Previos

Para ejecutar este proyecto necesitas:

- Python 3.7 o superior
- Librerías: TensorFlow, NumPy, Flask
- Archivos del modelo (ver abajo)

## 📦 Archivos del Modelo

Para que el proyecto funcione correctamente, necesitas los siguientes archivos del modelo:

```
src/lstm_llm/models/
├── final_token_model_spanish.keras   # Modelo LSTM pre-entrenado
└── token_vocabulary.json             # Vocabulario de tokens
```

> **Nota**: Si no tienes estos archivos, puedes entrenar tu propio modelo o solicitarlos al autor.

## 🚀 Instalación y Ejecución

1. **Instalar dependencias**:
   ```bash
   pip install tensorflow numpy flask flask-cors
   ```

2. **Colocar los archivos del modelo** en el directorio `src/lstm_llm/models/`

3. **Ejecutar el servidor**:
   ```bash
   cd src/lstm_llm
   python app.py
   ```

4. **Acceder a la interfaz web**: Abrir http://localhost:5000 en tu navegador

## 🧪 Experimentación

Puedes experimentar con el modelo ajustando varios parámetros:

1. **Temperatura**:
   - Valores más altos (>1.0) generan texto más creativo pero menos coherente
   - Valores más bajos (<1.0) producen texto más predecible y estructurado

2. **Longitud del texto**:
   - Puedes controlar cuántos tokens (palabras) generar
   - Textos más largos pueden perder coherencia gradualmente

3. **Prompt inicial**:
   - El texto inicial influye significativamente en el resultado
   - Prueba diferentes prompts para obtener resultados variados

## 🔧 Estructura del Proyecto

```
src/lstm_llm/
├── app.py                 # Servidor Flask y API
├── lstm_model.py          # Clase para manejar el modelo LSTM
├── templates/             # Plantillas HTML
│   └── index.html         # Interfaz principal
├── static/                # Archivos estáticos
│   ├── css/               # Estilos CSS
│   │   └── styles.css     # Estilos de la interfaz
│   └── js/                # JavaScript
│       └── app.js         # Lógica de la interfaz
└── models/                # Archivos del modelo
    ├── final_token_model_spanish.keras
    └── token_vocabulary.json
```

## 💡 Ideas para Extender el Proyecto

1. **Entrenamiento personalizado**: Entrena el modelo con otros libros o fuentes de texto
2. **Mejoras en la interfaz**: Añade opciones para guardar/exportar el texto generado
3. **Análisis de sentimiento**: Analiza el tono emocional del texto generado
4. **Generación guiada**: Implementa opciones para guiar la generación con restricciones
5. **Comparación de modelos**: Añade otros tipos de modelos (Markov, GPT, etc.) para comparar

## 📚 Recursos Adicionales

- [Documentación de TensorFlow sobre LSTM](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM)
- [Entendiendo las Redes LSTM](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Tutorial sobre Generación de Texto](https://www.tensorflow.org/text/tutorials/text_generation)

## 📄 Licencia

Este proyecto se distribuye bajo licencia MIT.

---

¡Disfruta experimentando con la generación de texto basada en LSTM! Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en este repositorio. 