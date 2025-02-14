import time
import random

class RRHHBot:
    def __init__(self):
        # Preguntas frecuentes y sus respuestas
        self.preguntas = {
            1: "¿Cuál es el proceso para solicitar vacaciones?",
            2: "¿Cómo solicito un certificado de trabajo?",
            3: "¿Cuál es el proceso de reembolso de gastos?",
            4: "¿Cómo reporto una ausencia por enfermedad?",
            5: "¿Cuál es la política de trabajo remoto?",
            6: "¿Cómo accedo a mis recibos de nómina?",
            7: "¿Cuál es el proceso de evaluación de desempeño?",
            8: "¿Cómo solicito un permiso especial?",
            9: "¿Cuál es la política de horas extras?",
            10: "¿Cómo funciona el seguro médico de la empresa?"
        }
        
        # Respuestas detalladas
        self.respuestas = {
            1: """El proceso para solicitar vacaciones es el siguiente:
1. Ingrese al portal de empleados
2. Complete el formulario de solicitud con 15 días de anticipación
3. Su supervisor recibirá la solicitud para aprobación
4. Recibirá un email con la confirmación""",
            
            2: """Para solicitar un certificado de trabajo:
1. Envíe un email a rrhh@empresa.com
2. Especifique el tipo de certificado (laboral, ingresos, etc.)
3. El documento estará listo en 48 horas hábiles
4. Retire el certificado en oficina de RRHH""",
            
            3: """El proceso de reembolso de gastos requiere:
1. Conservar todas las facturas originales
2. Completar el formulario de reembolso
3. Adjuntar las facturas escaneadas
4. El reembolso se procesa en la siguiente nómina""",
            
            4: """Para reportar una ausencia por enfermedad:
1. Notifique a su supervisor directo
2. Envíe el certificado médico a rrhh@empresa.com
3. Complete el formulario de ausencia al reintegrarse
4. Adjunte documentación médica original""",
            
            5: """La política de trabajo remoto establece:
1. Disponible para posiciones elegibles
2. Requiere aprobación del supervisor
3. Debe mantener conectividad y disponibilidad
4. Evaluación trimestral del arrangement""",
            
            6: """Para acceder a sus recibos de nómina:
1. Ingrese al portal de empleados
2. Sección "Mis Documentos"
3. Subsección "Recibos de Nómina"
4. Disponibles los últimos 12 meses""",
            
            7: """El proceso de evaluación de desempeño incluye:
1. Autoevaluación (Enero)
2. Evaluación del supervisor (Febrero)
3. Reunión de feedback (Marzo)
4. Plan de desarrollo (Abril)""",
            
            8: """Para solicitar un permiso especial:
1. Complete el formulario de permisos
2. Adjunte documentación de respaldo
3. Envíe a su supervisor para aprobación
4. RRHH procesará la solicitud en 48h""",
            
            9: """La política de horas extras establece:
1. Deben ser pre-aprobadas por supervisor
2. Se pagan al 150% en días hábiles
3. Se pagan al 200% en feriados
4. Se registran en el sistema de horarios""",
            
            10: """El seguro médico de la empresa:
1. Cobertura desde el primer día
2. Incluye grupo familiar directo
3. Red de prestadores preferencial
4. Reintegro de gastos en 7 días"""}
        
        self.mensajes_transicion = [
            "¿Hay algo más que pueda ayudarte?",
            "¿Tienes otra consulta?",
            "¿Necesitas información adicional?",
            "¿Puedo ayudarte con algo más?",
            "¿Deseas consultar sobre otro tema?"
        ]

    def mostrar_menu(self):
        print("\nPor favor, seleccione una opción (1-10) o '0' para salir:")
        for num, pregunta in self.preguntas.items():
            print(f"{num}. {pregunta}")
        print("0. Salir")

    def formatear_mensaje(self, mensaje):
        print(f"\nBot RRHH: {mensaje}")
        time.sleep(1)

    def procesar_consulta(self, opcion):
        try:
            opcion = int(opcion)
            if opcion == 0:
                self.formatear_mensaje("¡Gracias por usar el asistente de RRHH! ¡Hasta pronto!")
                return False
            elif opcion in self.respuestas:
                self.formatear_mensaje(self.respuestas[opcion])
                time.sleep(1)
                self.formatear_mensaje(random.choice(self.mensajes_transicion))
                return True
            else:
                self.formatear_mensaje("Por favor, seleccione una opción válida (0-10)")
                return True
        except ValueError:
            self.formatear_mensaje("Por favor, ingrese solo números del 0 al 10")
            return True

def main():
    print("\n" + "*" * 78)
    print("*  Asistente Virtual de RRHH")
    print("*  Bot de consultas sobre procesos y políticas de Recursos Humanos")
    print("*" + "*" * 71)
    
    bot = RRHHBot()
    bot.formatear_mensaje("¡Hola! Soy tu asistente virtual de RRHH.")
    bot.formatear_mensaje("Puedo ayudarte con consultas sobre procesos y políticas de la empresa.")
    
    continuar = True
    while continuar:
        bot.mostrar_menu()
        entrada = input("\nUsuario: ").strip()
        continuar = bot.procesar_consulta(entrada)

if __name__ == "__main__":
    main() 