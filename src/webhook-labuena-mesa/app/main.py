from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv

from .database import DatabaseManager
from .models import MemberRequest, MemberResponse
from .utils import format_dialogflow_response

load_dotenv()

app = FastAPI(title="La Buena Mesa Webhook")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DatabaseManager()

@app.get("/")
async def root():
    return {"message": "Webhook para La Buena Mesa activo"}

@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    """
    Endpoint para recibir solicitudes de Dialogflow
    """
    req_data = await request.json()
    
    # Extraer la intención y parámetros
    query_result = req_data.get("queryResult", {})
    intent = query_result.get("intent", {}).get("displayName", "")
    
    # Verificar si es la intención de registro
    if intent == "register_club_member":
        # Extraer parámetros
        parameters = query_result.get("parameters", {})
        
        # Extraer valores correctamente de los objetos
        nombre = parameters.get("nombre", {}).get("name", "") if isinstance(parameters.get("nombre"), dict) else parameters.get("nombre", "")
        email = parameters.get("email", {}).get("email", "") if isinstance(parameters.get("email"), dict) else parameters.get("email", "")
        telefono = parameters.get("telefono", {}).get("number", "") if isinstance(parameters.get("telefono"), dict) else parameters.get("telefono", "")
        
        # Registrar miembro
        result = db.add_member(nombre, email, telefono)
        
        # Formatear respuesta para Dialogflow
        return format_dialogflow_response(result)
    
    # Respuesta por defecto para otras intenciones
    return {"fulfillmentText": "Lo siento, no puedo procesar esta solicitud."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
