# Curso de Inteligencia Artificial y Chatbots

Este repositorio contiene ejemplos prácticos de chatbots e inteligencia artificial. Está diseñado para ser accesible incluso si nunca has programado antes.

## 🤖 Proyectos Disponibles

### 1. ELIZA - Simulador de Psicoterapeuta
Una recreación en español del famoso chatbot ELIZA de 1966, que simula ser un psicoterapeuta rogeriano.

## 🚀 Cómo Empezar

### Paso 1: Preparar tu Computadora

1. **Instalar Python**
   - Ve a [python.org](https://www.python.org/downloads/)
   - Descarga la última versión de Python para tu sistema operativo
   - Durante la instalación, **¡importante!** marca la casilla que dice "Add Python to PATH"

2. **Descargar este Proyecto**
   - En la parte superior de esta página, busca el botón verde que dice "Code"
   - Haz clic y selecciona "Download ZIP"
   - Descomprime el archivo descargado en una carpeta de tu elección

### Paso 2: Preparar el Proyecto

1. **Abrir la Terminal** (También llamada Símbolo del Sistema o PowerShell)
   - En Windows: Presiona `Windows + R`, escribe `cmd` y presiona Enter
   - En Mac: Busca "Terminal" en Spotlight (⌘ + Espacio)

2. **Navegar a la Carpeta del Proyecto**
   ```bash
   cd ruta/a/la/carpeta/chatbots
   ```
   (Reemplaza "ruta/a/la/carpeta" con la ubicación donde descomprimiste el proyecto)

3. **Crear un Entorno Virtual**
   ```bash
   python -m venv venv
   ```

4. **Activar el Entorno Virtual**
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Instalar las Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Paso 3: Ejecutar los Proyectos

#### Para usar ELIZA:
1. Navega a la carpeta del proyecto (si no estás ya en ella)
2. Asegúrate de que el entorno virtual está activado (verás `(venv)` al inicio de la línea de comandos)
3. Ejecuta:
   ```bash
   python src/eliza.py
   ```
4. ¡Comienza a chatear con ELIZA! Escribe tus mensajes y presiona Enter
5. Para terminar la conversación, escribe "adios" o "salir"

## 📝 Notas Importantes

- Cada vez que quieras usar los chatbots, necesitarás activar el entorno virtual primero
- Si cierras la terminal, necesitarás volver a activar el entorno virtual
- Los chatbots funcionan mejor si escribes en español y con buena ortografía
- No es necesario usar mayúsculas o signos de puntuación, pero los mensajes deben ser claros

## ❓ Solución de Problemas Comunes

1. **"Python no está reconocido como un comando..."**
   - Necesitas reinstalar Python y asegurarte de marcar "Add Python to PATH"

2. **"No se puede activar el entorno virtual"**
   - Asegúrate de estar en la carpeta correcta
   - Verifica que Python está instalado correctamente

3. **El programa se cierra inmediatamente**
   - Ejecuta el programa desde la terminal, no haciendo doble clic en el archivo

## 🤝 Contribuir

Si encuentras algún error o tienes sugerencias, por favor abre un "Issue" en GitHub.

## 📜 Licencia

Este proyecto es software libre y puede ser utilizado con fines educativos. 