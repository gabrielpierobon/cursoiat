import time
import re

class IABot:
    def __init__(self):
        # Estados posibles del bot
        self.estados = {
            'inicio': self.saludo_inicial,
            'pedir_nombre': self.pedir_nombre,
            'pedir_apellido': self.pedir_apellido,
            'pedir_edad': self.pedir_edad,
            'pedir_email': self.pedir_email,
            'confirmar_datos': self.confirmar_datos,
            'despedida': self.despedida
        }
        
        # Estado actual del bot
        self.estado_actual = 'inicio'
        
        # Datos del usuario
        self.datos_usuario = {
            'nombre': '',
            'apellido': '',
            'edad': '',
            'email': ''
        }
        
        # Respuestas predefinidas para errores
        self.respuestas_error = {
            'nombre': "Lo siento, el nombre solo debe contener letras. Por favor, intente nuevamente.",
            'apellido': "Lo siento, el apellido solo debe contener letras. Por favor, intente nuevamente.",
            'edad': "Por favor, ingrese una edad válida entre 18 y 99 años.",
            'email': "Por favor, ingrese un email válido.",
            'general': "No entiendo su respuesta. Por favor, siga las instrucciones."
        }

    def formatear_mensaje(self, mensaje):
        print(f"\nBot: {mensaje}")
        time.sleep(1)

    def validar_nombre(self, texto):
        return bool(re.match(r'^[A-Za-zÁ-Úá-úñÑ\s]{2,30}$', texto))

    def validar_edad(self, texto):
        try:
            edad = int(texto)
            return 18 <= edad <= 99
        except ValueError:
            return False

    def validar_email(self, texto):
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', texto))

    # Estados del bot
    def saludo_inicial(self, _=None):
        self.formatear_mensaje("¡Hola! Soy el asistente de registro para el curso de IA.")
        self.formatear_mensaje("Para comenzar el proceso de inscripción, necesitaré algunos datos.")
        self.estado_actual = 'pedir_nombre'
        return "Por favor, ingrese su nombre:"

    def pedir_nombre(self, entrada):
        if self.validar_nombre(entrada):
            self.datos_usuario['nombre'] = entrada
            self.estado_actual = 'pedir_apellido'
            return "Gracias. Ahora, por favor ingrese su apellido:"
        return self.respuestas_error['nombre']

    def pedir_apellido(self, entrada):
        if self.validar_nombre(entrada):
            self.datos_usuario['apellido'] = entrada
            self.estado_actual = 'pedir_edad'
            return "¿Cuál es su edad?"
        return self.respuestas_error['apellido']

    def pedir_edad(self, entrada):
        if self.validar_edad(entrada):
            self.datos_usuario['edad'] = entrada
            self.estado_actual = 'pedir_email'
            return "Por favor, ingrese su dirección de email:"
        return self.respuestas_error['edad']

    def pedir_email(self, entrada):
        if self.validar_email(entrada):
            self.datos_usuario['email'] = entrada
            self.estado_actual = 'confirmar_datos'
            return self.mostrar_resumen()
        return self.respuestas_error['email']

    def mostrar_resumen(self):
        resumen = "\nPor favor, confirme si los siguientes datos son correctos:\n"
        resumen += f"Nombre: {self.datos_usuario['nombre']}\n"
        resumen += f"Apellido: {self.datos_usuario['apellido']}\n"
        resumen += f"Edad: {self.datos_usuario['edad']}\n"
        resumen += f"Email: {self.datos_usuario['email']}\n"
        resumen += "\n¿Los datos son correctos? (si/no)"
        return resumen

    def confirmar_datos(self, entrada):
        if entrada.lower() == 'si':
            self.estado_actual = 'despedida'
            return "¡Excelente! Sus datos han sido registrados correctamente."
        elif entrada.lower() == 'no':
            self.estado_actual = 'inicio'
            self.datos_usuario = {'nombre': '', 'apellido': '', 'edad': '', 'email': ''}
            return "Entiendo. Comenzaremos el proceso nuevamente."
        return "Por favor, responda 'si' o 'no'."

    def despedida(self, _=None):
        self.formatear_mensaje("Gracias por registrarse en nuestro curso.")
        self.formatear_mensaje("Recibirá un email con las instrucciones para comenzar.")
        return "¡Que tenga un excelente día!"

    def procesar_entrada(self, entrada):
        # Obtener la función correspondiente al estado actual
        funcion_estado = self.estados[self.estado_actual]
        # Procesar la entrada según el estado
        return funcion_estado(entrada)

def main():
    print("\n" + "*" * 78)
    print("*  Asistente de Registro - Bot Básico")
    print("*  Un ejemplo de chatbot con interacciones preprogramadas")
    print("*" + "*" * 71)
    
    bot = IABot()
    # Mostrar saludo inicial
    respuesta = bot.saludo_inicial()
    print(f"\nBot: {respuesta}")
    
    while bot.estado_actual != 'despedida':
        entrada = input("\nUsuario: ").strip()
        respuesta = bot.procesar_entrada(entrada)
        print(f"\nBot: {respuesta}")
        
        if bot.estado_actual == 'despedida':
            break

if __name__ == "__main__":
    main() 