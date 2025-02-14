import time
import random
import re
import signal
from datetime import datetime, timedelta
import threading
import queue

class InversorIA:
    def __init__(self):
        # Perfil del inversor
        self.perfil_inversor = {
            'riesgo': 'moderado',  # conservador, moderado, agresivo
            'horizonte': 'medio',   # corto, medio, largo
            'objetivo': 'crecimiento', # crecimiento, dividendos, mixto
            'capital_inicial': 10000,
            'inversion_mensual': 1000,
            'preferencias': {
                'sectores': ['tecnología', 'salud', 'finanzas'],
                'tipo_activos': ['acciones', 'ETFs', 'bonos'],
                'mercados': ['USA', 'Europa', 'Emergentes']
            }
        }
        
        # Simulación de mercado y activos
        self.activos = {
            'acciones': {
                'AAPL': {
                    'nombre': 'Apple Inc.',
                    'precio': 175.50,
                    'sector': 'tecnología',
                    'riesgo': 'moderado',
                    'dividendo': 0.5,
                    'mercado': 'USA'
                },
                'MSFT': {
                    'nombre': 'Microsoft Corp.',
                    'precio': 320.75,
                    'sector': 'tecnología',
                    'riesgo': 'moderado',
                    'dividendo': 0.8,
                    'mercado': 'USA'
                },
                'JPM': {
                    'nombre': 'JPMorgan Chase',
                    'precio': 145.25,
                    'sector': 'finanzas',
                    'riesgo': 'moderado',
                    'dividendo': 2.5,
                    'mercado': 'USA'
                }
            },
            'ETFs': {
                'VTI': {
                    'nombre': 'Vanguard Total Stock Market',
                    'precio': 220.30,
                    'tipo': 'índice',
                    'riesgo': 'moderado',
                    'dividendo': 1.5,
                    'mercado': 'USA'
                },
                'VEA': {
                    'nombre': 'Vanguard Developed Markets',
                    'precio': 45.80,
                    'tipo': 'internacional',
                    'riesgo': 'moderado',
                    'dividendo': 2.0,
                    'mercado': 'Europa'
                }
            },
            'bonos': {
                'AGG': {
                    'nombre': 'iShares Core U.S. Aggregate Bond',
                    'precio': 98.45,
                    'tipo': 'gubernamental',
                    'riesgo': 'bajo',
                    'rendimiento': 3.5,
                    'mercado': 'USA'
                }
            }
        }

        # Cartera actual del usuario
        self.cartera = {
            'efectivo': 10000,
            'posiciones': {},
            'valor_total': 10000,
            'rendimiento': 0
        }

        # Patrones de intención
        self.intenciones = {
            'perfil_riesgo': {
                'patrones': [
                    r'(?i).*(?:cambiar|modificar|actualizar).*(?:perfil|riesgo).*(?:a|por) (conservador|moderado|agresivo)',
                    r'(?i).*(?:quiero|prefiero) (?:ser|invertir).*(?:más|menos|de forma) (conservador|moderado|agresivo)',
                    r'(?i)^(?:perfil|riesgo) (conservador|moderado|agresivo)$'
                ],
                'entidades_requeridas': ['nivel_riesgo'],
                'respuesta_faltantes': "¿Qué perfil de riesgo prefieres? (conservador/moderado/agresivo)"
            },
            'comprar_activo': {
                'patrones': [
                    r'(?i).*(?:comprar|adquirir|invertir en) ([A-Z]+)',
                    r'(?i).*(?:comprar|invertir).*(?:acciones de) ([A-Z]+)',
                    r'(?i)^(?:comprar|compra) ([A-Z]+)$'
                ],
                'entidades_requeridas': ['simbolo', 'cantidad'],
                'respuesta_faltantes': "¿Qué activo te gustaría comprar? (Ejemplo: AAPL, MSFT, VTI)"
            },
            'vender_activo': {
                'patrones': [
                    r'(?i).*(?:vender|liquidar) ([A-Z]+)',
                    r'(?i).*(?:vender|liquidar).*(?:acciones de) ([A-Z]+)',
                    r'(?i)^(?:vender|venta) ([A-Z]+)$'
                ],
                'entidades_requeridas': ['simbolo', 'cantidad'],
                'respuesta_faltantes': "¿Qué activo te gustaría vender?"
            },
            'consultar_cartera': {
                'patrones': [
                    r'(?i).*(?:ver|mostrar|consultar).*(?:cartera|portfolio|inversiones)',
                    r'(?i).*(?:cómo va|estado de).*(?:mi cartera|mis inversiones)',
                    r'(?i)^(?:cartera|portfolio|inversiones)$'
                ],
                'entidades_requeridas': [],
                'respuesta_faltantes': None
            }
        }

        # Estado de la operación
        self.estado_operacion = {
            'tipo': None,  # compra, venta
            'simbolo': None,
            'cantidad': None,
            'precio': None,
            'total': None,
            'confirmada': False
        }

        # Estado de la conversación
        self.estado_conversacion = {
            'intencion_actual': None,
            'entidades_detectadas': {},
            'siguiente_estado': None,
            'esperando_confirmacion': False
        }

    def procesar_entrada(self, texto):
        """Procesa la entrada del usuario"""
        # Continuar si hay una operación en curso
        if self.estado_operacion['tipo'] and not self.estado_operacion['confirmada']:
            return self.continuar_operacion(texto)

        # Detectar intención
        for intencion, config in self.intenciones.items():
            for patron in config['patrones']:
                match = re.match(patron, texto)
                if match:
                    return self.manejar_intencion(intencion, match)

        return "No he entendido tu solicitud. ¿Puedes reformularla?"

    def manejar_intencion(self, intencion, match):
        """Maneja la intención detectada"""
        if intencion == 'consultar_cartera':
            return self.mostrar_cartera()
        
        if intencion == 'perfil_riesgo':
            nivel = match.group(1).lower()
            return self.actualizar_perfil_riesgo(nivel)
        
        # Para compra/venta de activos
        simbolo = match.group(1).upper()
        if intencion in ['comprar_activo', 'vender_activo']:
            return self.iniciar_operacion(intencion, simbolo)
        
        return "No he podido procesar tu solicitud. ¿Puedes reformularla?"

    def iniciar_operacion(self, tipo, simbolo):
        """Inicia una operación de compra/venta"""
        # Validar el símbolo
        activo = self.buscar_activo(simbolo)
        if not activo:
            return f"Lo siento, no encontré el activo {simbolo}. Activos disponibles: {', '.join(self.obtener_simbolos_disponibles())}"
        
        self.estado_operacion = {
            'tipo': 'compra' if tipo == 'comprar_activo' else 'venta',
            'simbolo': simbolo,
            'activo': activo,
            'cantidad': None,
            'precio': activo['precio'],
            'total': None,
            'confirmada': False
        }
        
        return f"¿Cuántas unidades de {simbolo} ({activo['nombre']}) quieres {'comprar' if tipo == 'comprar_activo' else 'vender'}? (Precio actual: ${activo['precio']})"

    def continuar_operacion(self, texto):
        """Continúa una operación en curso"""
        if not self.estado_operacion['cantidad']:
            try:
                cantidad = int(texto)
                if cantidad <= 0:
                    return "Por favor, ingresa una cantidad válida mayor a 0."
                
                self.estado_operacion['cantidad'] = cantidad
                self.estado_operacion['total'] = cantidad * self.estado_operacion['precio']
                
                # Validar la operación
                if self.estado_operacion['tipo'] == 'compra':
                    if self.estado_operacion['total'] > self.cartera['efectivo']:
                        return f"No tienes suficiente efectivo para esta operación. Máximo posible: {int(self.cartera['efectivo'] / self.estado_operacion['precio'])} unidades"
                else:  # venta
                    posicion_actual = self.cartera['posiciones'].get(self.estado_operacion['simbolo'], 0)
                    if cantidad > posicion_actual:
                        return f"No tienes suficientes unidades. Posición actual: {posicion_actual}"
                
                return self.mostrar_confirmacion_operacion()
            
            except ValueError:
                return "Por favor, ingresa un número válido."
        
        # Procesar confirmación
        respuesta = texto.lower()
        if respuesta in ['si', 'sí', 'confirmar']:
            return self.ejecutar_operacion()
        elif respuesta in ['no', 'cancelar']:
            self.estado_operacion = {'tipo': None, 'simbolo': None, 'cantidad': None, 'precio': None, 'total': None, 'confirmada': False}
            return "Operación cancelada. ¿Puedo ayudarte con algo más?"
        else:
            return "Por favor, responde 'si' para confirmar o 'no' para cancelar."

    def mostrar_confirmacion_operacion(self):
        """Muestra el resumen de la operación para confirmar"""
        op = self.estado_operacion
        return f"""Resumen de la operación:
Tipo: {op['tipo'].upper()}
Activo: {op['simbolo']} ({op['activo']['nombre']})
Cantidad: {op['cantidad']}
Precio unitario: ${op['precio']}
Total: ${op['total']}

¿Confirmas la operación? (si/no)"""

    def ejecutar_operacion(self):
        """Ejecuta la operación confirmada"""
        op = self.estado_operacion
        
        if op['tipo'] == 'compra':
            self.cartera['efectivo'] -= op['total']
            if op['simbolo'] in self.cartera['posiciones']:
                self.cartera['posiciones'][op['simbolo']] += op['cantidad']
            else:
                self.cartera['posiciones'][op['simbolo']] = op['cantidad']
        else:  # venta
            self.cartera['efectivo'] += op['total']
            self.cartera['posiciones'][op['simbolo']] -= op['cantidad']
            if self.cartera['posiciones'][op['simbolo']] == 0:
                del self.cartera['posiciones'][op['simbolo']]
        
        # Actualizar valor total
        self.actualizar_valor_cartera()
        
        # Limpiar estado
        resultado = f"Operación completada exitosamente. Nuevo saldo en efectivo: ${self.cartera['efectivo']:.2f}"
        self.estado_operacion = {'tipo': None, 'simbolo': None, 'cantidad': None, 'precio': None, 'total': None, 'confirmada': False}
        
        return resultado

    def mostrar_cartera(self):
        """Muestra el estado actual de la cartera"""
        self.actualizar_valor_cartera()
        
        respuesta = "\nEstado actual de tu cartera:\n"
        respuesta += f"Efectivo disponible: ${self.cartera['efectivo']:.2f}\n\n"
        
        if self.cartera['posiciones']:
            respuesta += "Posiciones:\n"
            for simbolo, cantidad in self.cartera['posiciones'].items():
                activo = self.buscar_activo(simbolo)
                valor = cantidad * activo['precio']
                respuesta += f"- {simbolo} ({activo['nombre']}): {cantidad} unidades - Valor: ${valor:.2f}\n"
        else:
            respuesta += "No tienes posiciones abiertas.\n"
        
        respuesta += f"\nValor total de la cartera: ${self.cartera['valor_total']:.2f}"
        return respuesta

    def actualizar_valor_cartera(self):
        """Actualiza el valor total de la cartera"""
        valor = self.cartera['efectivo']
        for simbolo, cantidad in self.cartera['posiciones'].items():
            activo = self.buscar_activo(simbolo)
            valor += cantidad * activo['precio']
        self.cartera['valor_total'] = valor

    def buscar_activo(self, simbolo):
        """Busca un activo por su símbolo"""
        for categoria in self.activos.values():
            if simbolo in categoria:
                return categoria[simbolo]
        return None

    def obtener_simbolos_disponibles(self):
        """Obtiene la lista de símbolos disponibles"""
        simbolos = []
        for categoria in self.activos.values():
            simbolos.extend(categoria.keys())
        return simbolos

def simular_evento_mercado():
    """Simula eventos aleatorios del mercado"""
    eventos = [
        {
            'tipo': 'caida_precio',
            'activo': 'AAPL',
            'cambio': -5.2,
            'mensaje': "Detecto una caída significativa en Apple (-5.2%). Podría ser una oportunidad de compra."
        },
        {
            'tipo': 'subida_precio',
            'activo': 'MSFT',
            'cambio': 3.8,
            'mensaje': "Microsoft está subiendo fuertemente (+3.8%). ¿Te gustaría tomar algunas ganancias?"
        },
        {
            'tipo': 'noticia',
            'activo': 'JPM',
            'mensaje': "Noticias positivas para JPMorgan: han superado las expectativas de beneficios este trimestre."
        },
        {
            'tipo': 'alerta_tecnica',
            'activo': 'VTI',
            'mensaje': "El ETF VTI está cerca de un soporte técnico importante. Podría ser un buen punto de entrada."
        }
    ]
    return random.choice(eventos)

def input_timeout(prompt, timeout=30):
    """Input con timeout multiplataforma"""
    print(prompt, end='', flush=True)
    print("\nTienes 30 segundos para analizar esta oportunidad o te enviaré los detalles por email...")
    respuesta = queue.Queue()
    
    def get_input():
        respuesta.put(input())
    
    # Crear thread para input
    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    
    # Mostrar cuenta regresiva mientras esperamos
    for i in range(timeout, 0, -1):
        if not thread.is_alive():  # Si el usuario ya respondió
            try:
                return respuesta.get_nowait()
            except queue.Empty:
                pass
        print(f"\rTiempo para analizar: {i} segundos...   ", end='', flush=True)
        time.sleep(1)
    
    print("\r" + " " * 50, end='\r')  # Limpiar línea de cuenta regresiva
    print("\nInversorIA: Entiendo que necesitas más tiempo para analizar esta oportunidad.")
    print("          Preparando informe detallado con análisis técnico y fundamental...")
    time.sleep(2)
    print("          ✉️ Email enviado exitosamente a usuario@ejemplo.com")
    print("          Incluye: análisis completo, gráficos y recomendaciones específicas")
    time.sleep(1)
    print("          Continuando con el monitoreo del mercado...")
    return "timeout"

def simular_siguiente_evento():
    """Simula el siguiente evento del mercado"""
    eventos = [
        {
            'timestamp': '[09:45 AM]',
            'tipo': '📊 ACTUALIZACIÓN DE MERCADO',
            'mensaje': [
                "S&P 500 recuperándose (+0.5%)",
                "Volumen de mercado normalizándose"
            ],
            'es_oportunidad': False
        },
        {
            'timestamp': '[10:15 AM]',
            'tipo': '🚨 ALERTA URGENTE',
            'mensaje': [
                "Microsoft (MSFT) rompe resistencia clave",
                "Volumen 65% superior a la media",
                "Señales técnicas muy positivas"
            ],
            'es_oportunidad': True
        },
        {
            'timestamp': '[10:30 AM]',
            'tipo': '📰 NOTICIA RELEVANTE',
            'mensaje': [
                "FED anuncia mantener tasas de interés",
                "Mercados reaccionando positivamente",
                "Sectores defensivos mostrando fortaleza"
            ],
            'es_oportunidad': False
        }
    ]
    return random.choice(eventos)

def mostrar_evento(evento):
    """Muestra un evento del mercado"""
    print(f"\n{evento['timestamp']} {evento['tipo']}")
    print("InversorIA: Detectando nuevo movimiento en el mercado...")
    time.sleep(1.5)
    for linea in evento['mensaje']:
        print(f"          - {linea}")
    
    if evento['es_oportunidad']:
        # Mostrar opciones solo si es una oportunidad
        print("\nOpciones disponibles:")
        print("1. Saber más sobre esta oportunidad")
        print("2. Ver análisis técnico")
        print("3. Ver análisis fundamental")
        print("4. Realizar operación")
        print("5. Continuar monitoreando")
        print("6. Salir")
        return True
    else:
        print("\nInversorIA: Continuando monitoreo del mercado...")
        time.sleep(2)
        return False

def main():
    print("\n" + "*" * 78)
    print("*  InversorIA - Tu Asistente Virtual de Inversiones")
    print("*  Iniciando simulación de mercado...")
    print("*" + "*" * 71)
    
    asistente = InversorIA()
    print("\nCargando datos del mercado y conectando APIs...")
    time.sleep(2)
    
    # Simular apertura de mercado
    print("\nInversorIA: Mercados abriendo en:")
    for i in range(3, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n")
    
    print("InversorIA: ¡Mercados abiertos! Comenzando monitoreo en tiempo real...")
    time.sleep(1.5)
    
    # Simular día de trading
    print("\nInversorIA: Detectando condiciones iniciales del mercado...")
    time.sleep(2)
    print("InversorIA: Futuros del S&P 500 indican apertura positiva (+0.3%)")
    time.sleep(1.5)
    print("InversorIA: Mercados europeos operando al alza")
    time.sleep(2)
    
    # Primera alerta importante
    print("\n[09:31 AM] ⚠️ ALERTA DE MERCADO ⚠️")
    print("InversorIA: Detecto movimiento inusual en el sector tecnológico")
    time.sleep(1)
    print("          - Apple (AAPL) cae 3% en la apertura")
    print("          - Volumen de operaciones 40% superior al promedio")
    time.sleep(2)
    print("\nInversorIA: Analizando implicaciones para la cartera...")
    time.sleep(1.5)
    print("InversorIA: Recomendación: Considerar compra si el precio toca $170")

    while True:
        print("\nOpciones disponibles:")
        print("1. Saber más sobre esta oportunidad")
        print("2. Ver análisis técnico")
        print("3. Ver análisis fundamental")
        print("4. Realizar operación")
        print("5. Continuar monitoreando")
        print("6. Salir")

        opcion = input_timeout("\nTú: ")
        
        # Si hay timeout o usuario elige continuar monitoreando
        if opcion == "timeout" or opcion == "5":
            if opcion == "timeout":
                time.sleep(2)
            else:
                print("\nInversorIA: Continuando monitoreo del mercado...")
                time.sleep(2)
            
            # Mostrar siguiente evento
            evento = simular_siguiente_evento()
            es_oportunidad = mostrar_evento(evento)
            
            if es_oportunidad:
                # Iniciar nuevo ciclo de espera solo si es una oportunidad
                opcion = input_timeout("\nTú: ")
                if opcion == "timeout":
                    print("\nInversorIA: Entiendo que necesitas más tiempo para analizar esta oportunidad.")
                    print("          Te enviaré los detalles por email...")
                    time.sleep(2)
                    print("          ✉️ Email enviado exitosamente a usuario@ejemplo.com")
                    print("          Continuando con el monitoreo del mercado...")
                    time.sleep(2)
            continue
        
        if opcion == "1":
            print("\nInversorIA: Analizando el contexto completo...")
            time.sleep(1.5)
            print("""
La caída actual de Apple presenta una oportunidad interesante por varios factores:

1. Contexto de Mercado:
   - La caída no está relacionada con problemas fundamentales de la empresa
   - El sector tecnológico en general muestra fortaleza
   - Los resultados financieros del último trimestre superaron expectativas

2. Indicadores Técnicos:
   - El RSI está en zona de sobreventa (32)
   - El precio se acerca a la media móvil de 200 días
   - El volumen sugiere acumulación institucional

3. Catalizadores Próximos:
   - Presentación de nuevo producto en 2 semanas
   - Actualización de guidance fiscal en próxima conferencia
   - Posible ampliación del programa de recompra de acciones

¿Te gustaría profundizar en algún aspecto específico?
""")
            while True:
                print("\nPuedes preguntarme sobre:")
                print("1. Análisis técnico detallado")
                print("2. Situación fundamental")
                print("3. Riesgos potenciales")
                print("4. Volver al monitoreo")
                
                subopcion = input("\nTú: ").strip()
                
                if subopcion == "1":
                    print("""
Análisis Técnico Detallado:
- Soporte principal: $170 (coincide con retroceso Fibonacci 38.2%)
- Resistencias: $180 (corto plazo), $185 (objetivo técnico)
- Momentum: MACD muestra divergencia alcista
- Volatilidad: Bandas de Bollinger sugieren compresión
- Volumen: Perfil de volumen muestra fuerte soporte en $170-172
""")
                elif subopcion == "2":
                    print("""
Situación Fundamental:
- P/E Ratio: 28.5x (por debajo de la media histórica de 32x)
- Crecimiento de ingresos YoY: +12%
- Margen operativo: 30.2% (mejora vs trimestre anterior)
- Flujo de caja libre: $98B (récord histórico)
- Efectivo neto: $162B
- Dividendo actual: 0.5% (sostenible y en crecimiento)
""")
                elif subopcion == "3":
                    print("""
Riesgos Potenciales:
1. Corto Plazo:
   - Tensiones geopolíticas afectando cadena de suministro
   - Posible retraso en lanzamiento de nuevos productos
   - Presión regulatoria en mercados clave

2. Medio Plazo:
   - Competencia creciente en servicios
   - Saturación del mercado de smartphones
   - Riesgo de tipo de cambio en mercados internacionales

3. Mitigantes:
   - Fuerte posición de efectivo
   - Diversificación de proveedores
   - Lealtad de marca sólida
""")
                elif subopcion == "4":
                    print("\nVolviendo al monitoreo del mercado...")
                    break
        
        elif opcion == "2":
            print("""
Análisis Técnico Actual:
- Precio en soporte clave de $170
- RSI: 32 (zona de sobreventa)
- MACD: Cruce alcista formándose
- Volumen: 40% sobre la media
- Tendencia: Alcista en largo plazo, corrección en corto
""")
        
        elif opcion == "3":
            print("""
Análisis Fundamental:
- Beneficio por acción: $6.45 (+15% YoY)
- Flujo de caja libre: $98B
- Margen bruto: 43.2%
- Deuda/EBITDA: 1.2x
- Retorno sobre capital: 35.8%
""")
        
        elif opcion == "4":
            print("\nInversorIA: Iniciando proceso de operación...")
            print("\n¿Qué operación te gustaría realizar?")
            print("1. Comprar AAPL")
            print("2. Vender otra posición")
            print("3. Volver al menú anterior")
            
            op_tipo = input("\nTú: ").strip()
            
            if op_tipo == "1":
                print("\nInversorIA: Analizando mejor punto de entrada...")
                time.sleep(1.5)
                print("""
Recomendación de operación:
- Precio actual: $170
- Stop loss sugerido: $165 (-3%)
- Objetivo de precio: $180 (+6%)
- Ratio riesgo/beneficio: 1:2
""")
                print("\n¿Deseas proceder con la compra? (si/no)")
                if input("\nTú: ").strip().lower() in ['si', 'sí', 'yes']:
                    print("\n¿Cuántas acciones deseas comprar?")
                    cantidad = input("\nTú: ").strip()
                    try:
                        cantidad = int(cantidad)
                        total = cantidad * 170
                        print(f"\nResumen de la orden:")
                        print(f"- Compra de {cantidad} acciones de AAPL")
                        print(f"- Precio por acción: $170")
                        print(f"- Total de la operación: ${total}")
                        print("\n¿Confirmas la operación? (si/no)")
                        
                        if input("\nTú: ").strip().lower() in ['si', 'sí', 'yes']:
                            print("\nInversorIA: Ejecutando orden...")
                            time.sleep(2)
                            print("InversorIA: ¡Orden ejecutada con éxito!")
                            print(f"Se han comprado {cantidad} acciones de AAPL a $170")
                    except ValueError:
                        print("Por favor, ingresa un número válido de acciones.")
            continue
        
        elif opcion == "6":
            print("\nInversorIA: Finalizando sesión de trading...")
            time.sleep(1)
            print("InversorIA: Resumen del día:")
            print("          - Mercado cerró mixto")
            print("          - Principales movimientos monitoreados")
            print("          - Oportunidades identificadas: 3")
            print("\nInversorIA: ¡Hasta la próxima sesión!")
            break
        
        else:
            print("\nOpción no válida. Por favor, elige una opción del menú.")
            continue

if __name__ == "__main__":
    main() 