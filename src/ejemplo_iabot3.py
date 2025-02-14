import time
import re

class CreditoBot:
    def __init__(self):
        # Estados del proceso
        self.estados = {
            'inicio': self.saludo_inicial,
            'datos_personales': self.pedir_datos_personales,
            'tipo_credito': self.pedir_tipo_credito,
            'ingresos': self.pedir_ingresos,
            'antiguedad': self.pedir_antiguedad,
            'situacion_laboral': self.pedir_situacion_laboral,
            'deudas': self.pedir_deudas,
            'propiedad': self.pedir_propiedad,
            'monto': self.pedir_monto,
            'plazo': self.pedir_plazo,
            'resumen': self.mostrar_resumen,
            'despedida': self.despedida
        }
        
        self.estado_actual = 'inicio'
        self.datos = {}
        
        # Opciones predefinidas
        self.opciones = {
            'tipo_credito': {
                1: "Préstamo Personal",
                2: "Crédito Hipotecario",
                3: "Préstamo Automotriz"
            },
            'rango_ingresos': {
                1: "Menos de $50,000",
                2: "$50,000 - $100,000",
                3: "$100,000 - $150,000",
                4: "Más de $150,000"
            },
            'antiguedad': {
                1: "Menos de 1 año",
                2: "1-3 años",
                3: "3-5 años",
                4: "Más de 5 años"
            },
            'situacion_laboral': {
                1: "Empleado tiempo completo",
                2: "Empleado tiempo parcial",
                3: "Independiente",
                4: "Jubilado"
            },
            'deudas': {
                1: "Sin deudas actuales",
                2: "Menos del 30% de mis ingresos",
                3: "Entre 30% y 50% de mis ingresos",
                4: "Más del 50% de mis ingresos"
            },
            'propiedad': {
                1: "Casa propia sin hipoteca",
                2: "Casa propia con hipoteca",
                3: "Alquiler",
                4: "Vivo con familiares"
            },
            'plazo': {
                1: "12 meses",
                2: "24 meses",
                3: "36 meses",
                4: "48 meses",
                5: "60 meses"
            }
        }

    def formatear_mensaje(self, mensaje):
        print(f"\nBot Créditos: {mensaje}")
        time.sleep(1)

    def mostrar_opciones(self, categoria):
        print("\nSeleccione una opción:")
        for num, opcion in self.opciones[categoria].items():
            print(f"{num}. {opcion}")

    def validar_nombre(self, texto):
        return bool(re.match(r'^[A-Za-zÁ-Úá-úñÑ\s]{2,30}$', texto))

    def validar_email(self, texto):
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', texto))

    def validar_telefono(self, texto):
        return bool(re.match(r'^\+?[\d\s-]{8,15}$', texto))

    # Estados del proceso
    def saludo_inicial(self, _=None):
        self.formatear_mensaje("¡Bienvenido al asistente de créditos!")
        self.formatear_mensaje("Lo guiaré en el proceso de solicitud de crédito.")
        self.estado_actual = 'datos_personales'
        return "Para comenzar, necesito algunos datos personales."

    def pedir_datos_personales(self, entrada=None):
        if entrada is None:
            self.formatear_mensaje("Por favor, ingrese su nombre completo:")
            return None
            
        if 'nombre' not in self.datos:
            if self.validar_nombre(entrada):
                self.datos['nombre'] = entrada
                return "Por favor, ingrese su email:"
            return "Nombre inválido. Por favor, ingrese solo letras."
            
        if 'email' not in self.datos:
            if self.validar_email(entrada):
                self.datos['email'] = entrada
                return "Por favor, ingrese su teléfono:"
            return "Email inválido. Por favor, intente nuevamente."
            
        if 'telefono' not in self.datos:
            if self.validar_telefono(entrada):
                self.datos['telefono'] = entrada
                self.estado_actual = 'tipo_credito'
                self.mostrar_opciones('tipo_credito')
                return "¿Qué tipo de crédito le interesa?"
            return "Teléfono inválido. Por favor, intente nuevamente."

    def pedir_tipo_credito(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['tipo_credito']:
                self.datos['tipo_credito'] = self.opciones['tipo_credito'][opcion]
                self.estado_actual = 'ingresos'
                self.mostrar_opciones('rango_ingresos')
                return "¿Cuál es su rango de ingresos mensuales?"
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_ingresos(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['rango_ingresos']:
                self.datos['ingresos'] = self.opciones['rango_ingresos'][opcion]
                self.estado_actual = 'antiguedad'
                self.mostrar_opciones('antiguedad')
                return "¿Cuál es su antigüedad laboral?"
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_antiguedad(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['antiguedad']:
                self.datos['antiguedad'] = self.opciones['antiguedad'][opcion]
                self.estado_actual = 'situacion_laboral'
                self.mostrar_opciones('situacion_laboral')
                return "¿Cuál es su situación laboral actual?"
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_situacion_laboral(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['situacion_laboral']:
                self.datos['situacion_laboral'] = self.opciones['situacion_laboral'][opcion]
                self.estado_actual = 'deudas'
                self.mostrar_opciones('deudas')
                return "¿Cuál es su nivel actual de endeudamiento?"
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_deudas(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['deudas']:
                self.datos['deudas'] = self.opciones['deudas'][opcion]
                self.estado_actual = 'propiedad'
                self.mostrar_opciones('propiedad')
                return "¿Cuál es su situación habitacional?"
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_propiedad(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['propiedad']:
                self.datos['propiedad'] = self.opciones['propiedad'][opcion]
                self.estado_actual = 'monto'
                return "¿Qué monto de crédito desea solicitar? (en pesos)"
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_monto(self, entrada):
        try:
            monto = float(entrada)
            if 10000 <= monto <= 1000000:
                self.datos['monto'] = monto
                self.estado_actual = 'plazo'
                self.mostrar_opciones('plazo')
                return "¿A qué plazo desea el crédito?"
            return "El monto debe estar entre $10,000 y $1,000,000"
        except ValueError:
            return "Por favor, ingrese solo números."

    def pedir_plazo(self, entrada):
        try:
            opcion = int(entrada)
            if opcion in self.opciones['plazo']:
                self.datos['plazo'] = self.opciones['plazo'][opcion]
                self.estado_actual = 'resumen'
                return self.mostrar_resumen()
            return "Por favor, seleccione una opción válida."
        except ValueError:
            return "Por favor, ingrese solo números."

    def mostrar_resumen(self, _=None):
        resumen = "\nResumen de su solicitud de crédito:"
        resumen += f"\nNombre: {self.datos['nombre']}"
        resumen += f"\nEmail: {self.datos['email']}"
        resumen += f"\nTeléfono: {self.datos['telefono']}"
        resumen += f"\nTipo de Crédito: {self.datos['tipo_credito']}"
        resumen += f"\nIngresos Mensuales: {self.datos['ingresos']}"
        resumen += f"\nAntigüedad Laboral: {self.datos['antiguedad']}"
        resumen += f"\nSituación Laboral: {self.datos['situacion_laboral']}"
        resumen += f"\nNivel de Endeudamiento: {self.datos['deudas']}"
        resumen += f"\nSituación Habitacional: {self.datos['propiedad']}"
        resumen += f"\nMonto Solicitado: ${self.datos['monto']:,.2f}"
        resumen += f"\nPlazo: {self.datos['plazo']}"
        
        self.estado_actual = 'despedida'
        return resumen + "\n\nPresione Enter para finalizar."

    def despedida(self, _=None):
        self.formatear_mensaje("¡Gracias por usar nuestro asistente de créditos!")
        self.formatear_mensaje("Un ejecutivo se pondrá en contacto con usted en las próximas 24 horas.")
        return "¡Que tenga un excelente día!"

    def procesar_entrada(self, entrada):
        funcion_estado = self.estados[self.estado_actual]
        return funcion_estado(entrada)

def main():
    print("\n" + "*" * 78)
    print("*  Asistente Virtual de Créditos Bancarios")
    print("*  Simulador de solicitud de crédito")
    print("*" + "*" * 71)
    
    bot = CreditoBot()
    respuesta = bot.saludo_inicial()
    print(f"\nBot Créditos: {respuesta}")
    
    while bot.estado_actual != 'despedida':
        entrada = input("\nUsuario: ").strip()
        respuesta = bot.procesar_entrada(entrada)
        if respuesta:
            print(f"\nBot Créditos: {respuesta}")

if __name__ == "__main__":
    main() 