def format_dialogflow_response(result):
    """
    Formatea la respuesta para Dialogflow según el resultado del registro
    """
    if result["success"] and result["is_new"]:
        fulfillment_text = (
            f"¡Felicidades! Ha sido registrado exitosamente en nuestro club de miembros. "
            f"Su código de descuento del 10% para su primera visita es: {result['voucher_code']}. "
            f"Muestre este código a nuestro personal al momento de solicitar la cuenta. "
            f"¿Puedo ayudarle con algo más?"
        )
    else:
        fulfillment_text = (
            f"{result['message']} "
            f"No se preocupe, todos los beneficios de miembro siguen activos con su cuenta existente. "
            f"¿Hay algo más en lo que pueda ayudarle?"
        )
    
    return {
        "fulfillmentText": fulfillment_text
    }
