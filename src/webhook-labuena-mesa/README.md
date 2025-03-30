# Webhook La Buena Mesa - Club de Miembros

Este webhook implementado con FastAPI gestiona el registro de miembros del club de La Buena Mesa, permitiendo a los usuarios recibir descuentos y ofertas especiales a través de un chatbot en Dialogflow.

## Requisitos Previos

- Python 3.10 o superior
- Cuenta en Dialogflow
- ngrok para pruebas locales

## Configuración del Entorno

1. **Clonar el repositorio y crear entorno virtual**:
```bash
# Crear y acceder al directorio del proyecto
mkdir webhook-labuena-mesa
cd webhook-labuena-mesa

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

2. **Instalar dependencias**:
```bash
pip install fastapi uvicorn python-dotenv "pydantic[email]" openpyxl
```

3. **Configurar variables de entorno**:
Crear archivo `.env` en la raíz del proyecto:
```
DB_FILE=data/members.xlsx
VOUCHER_PREFIX=LBM-
```

## Estructura del Proyecto

```
webhook-labuena-mesa/
├── venv/
├── .env
├── app/
│   ├── __init__.py
│   ├── database.py    # Gestión de base datos Excel
│   ├── models.py      # Modelos Pydantic
│   ├── utils.py       # Funciones auxiliares
│   └── main.py        # Aplicación FastAPI
├── data/
│   └── members.xlsx   # Base de datos de miembros
└── requirements.txt
```

## Ejecución Local

1. **Iniciar el servidor FastAPI**:
```bash
python -m uvicorn app.main:app --reload
```

2. **Exponer el servidor con ngrok**:
```bash
# En una nueva terminal
ngrok http 8000
```

## Configuración en Dialogflow

1. **Crear Intent `register_club_member`**:

   - **Frases de entrenamiento**:
     - "Quiero unirme al club de miembros"
     - "Cómo me registro como miembro"
     - "Me gustaría recibir ofertas especiales"
     - "¿Cómo me uno al club de fidelidad?"
     - "Quiero ser miembro del club"
     - "Me interesa el programa de descuentos"
     - "Quiero registrarme en el club"
     - "¿Tienen programa de fidelización?"
     - "Quiero descuentos especiales"
     - "Cómo me hago socio del restaurante"

   - **Parámetros**:
     - `nombre` (@sys.person) - Obligatorio
     - `email` (@sys.email) - Obligatorio
     - `telefono` (@sys.phone-number) - Obligatorio

2. **Configurar Webhook**:
   - En Dialogflow, ir a "Fulfillment"
   - Activar "Webhook"
   - URL: `https://tu-url-ngrok.ngrok-free.app/webhook`
   - Headers: No requeridos
   - Activar webhook para el intent `register_club_member`

## Ejemplos de Interacción

### Registro Exitoso
```
Usuario: Quiero unirme al club de miembros
Bot: Perfecto, vamos a registrarlo en nuestro club de miembros. ¿Cuál es su nombre completo?
Usuario: Juan Pérez
Bot: ¿Cuál es su dirección de correo electrónico?
Usuario: juan.perez@gmail.com
Bot: ¿Cuál es su número de teléfono?
Usuario: +34612345678
Bot: ¡Felicidades! Ha sido registrado exitosamente en nuestro club de miembros. 
     Su código de descuento del 10% para su primera visita es: LBM-A7B3C9D2. 
     Muestre este código a nuestro personal al momento de solicitar la cuenta.
```

### Usuario Ya Registrado
```
Usuario: Me gustaría recibir ofertas especiales
Bot: Perfecto, vamos a registrarlo en nuestro club de miembros. ¿Cuál es su nombre completo?
Usuario: María Rodríguez
Bot: ¿Cuál es su dirección de correo electrónico?
Usuario: maria.rodriguez@gmail.com
Bot: ¿Cuál es su número de teléfono?
Usuario: +34687654321
Bot: Este email o teléfono ya está registrado en nuestro club de miembros. 
     No se preocupe, todos los beneficios de miembro siguen activos con su cuenta existente.
```

## Notas Importantes

1. La URL de ngrok cambia cada vez que se reinicia el servicio. Actualizar en Dialogflow cuando sea necesario.
2. El archivo Excel se crea automáticamente en `data/members.xlsx` al iniciar el servidor.
3. Los códigos de descuento son únicos y tienen el formato `LBM-XXXXXXXX`.
4. El webhook maneja tanto respuestas simples como objetos complejos de Dialogflow para los parámetros.

## Endpoints Disponibles

- `GET /` - Verificar estado del servidor
- `POST /webhook` - Endpoint principal para Dialogflow

## Documentación API

Una vez iniciado el servidor, puedes acceder a:
- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

