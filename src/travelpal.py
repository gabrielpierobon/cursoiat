import time
import random
import re
from datetime import datetime, timedelta

class TravelPal:
    def __init__(self):
        # Simulación de base de datos de usuarios
        self.preferencias_usuario = {
            'asiento': 'ventana',
            'clase': 'económica',
            'comidas': 'regular',
            'tipo_hotel': '3 estrellas',
            'ultimo_destino': 'Madrid',
            'historial_busquedas': []
        }
        
        # Simulación de base de datos de vuelos
        self.vuelos_disponibles = {
            'Madrid': {
                'precio': {'económica': 500, 'business': 1500},
                'duracion': '2h 30m',
                'escalas': 0
            },
            'París': {
                'precio': {'económica': 600, 'business': 1800},
                'duracion': '2h 45m',
                'escalas': 0
            },
            'Londres': {
                'precio': {'económica': 550, 'business': 1600},
                'duracion': '2h 15m',
                'escalas': 0
            },
            'Roma': {
                'precio': {'económica': 450, 'business': 1400},
                'duracion': '2h',
                'escalas': 1
            },
            'Barcelona': {
                'precio': {'económica': 400, 'business': 1200},
                'duracion': '1h 30m',
                'escalas': 0
            },
            'Berlín': {
                'precio': {'económica': 700, 'business': 2100},
                'duracion': '3h',
                'escalas': 1
            },
            'Ámsterdam': {
                'precio': {'económica': 650, 'business': 1950},
                'duracion': '2h 45m',
                'escalas': 0
            },
            'Lisboa': {
                'precio': {'económica': 350, 'business': 1050},
                'duracion': '1h 15m',
                'escalas': 0
            }
        }
        
        # Simulación de base de datos de hoteles
        self.hoteles_disponibles = {
            'Madrid': [
                {'nombre': 'Gran Vía Hotel', 'estrellas': 4, 'precio': 150},
                {'nombre': 'Madrid Central', 'estrellas': 3, 'precio': 100},
                {'nombre': 'Luxury Palace', 'estrellas': 5, 'precio': 300}
            ],
            'Barcelona': [
                {'nombre': 'Barcelona Beach', 'estrellas': 4, 'precio': 180},
                {'nombre': 'Ramblas Suite', 'estrellas': 3, 'precio': 120},
                {'nombre': 'Catalonia Royal', 'estrellas': 5, 'precio': 350}
            ],
            'París': [
                {'nombre': 'Le Petit Hotel', 'estrellas': 3, 'precio': 180},
                {'nombre': 'Paris Elegance', 'estrellas': 4, 'precio': 250},
                {'nombre': 'Royal Paris', 'estrellas': 5, 'precio': 400}
            ],
            'Londres': [
                {'nombre': 'London Bridge Hotel', 'estrellas': 4, 'precio': 200},
                {'nombre': 'Westminster Inn', 'estrellas': 3, 'precio': 150},
                {'nombre': 'The Ritz', 'estrellas': 5, 'precio': 500}
            ]
        }
        
        # Intenciones y patrones de NLP simulados
        self.patrones = {
            'buscar_vuelo': r'(?i).*(?:vuelo|volar|viaje).*(?:a|hacia|para) ([A-Za-zÁ-úñÑ\s]+)',
            'consultar_precio': r'(?i).*(?:precio|costo|valor).*(?:a|de|para) ([A-Za-zÁ-úñÑ\s]+)',
            'buscar_hotel': r'(?i).*(?:hotel|alojamiento|hospedaje).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
            'cambiar_preferencias': r'(?i).*(?:prefiero|quiero|cambiar a) (ventana|pasillo|business|económica)',
            'consultar_actividades': r'(?i).*(?:hacer|actividades|turismo).*(?:en) ([A-Za-zÁ-úñÑ\s]+)'
        }
        
        # Actividades turísticas simuladas
        self.actividades = {
            'Madrid': [
                {'nombre': 'Visita al Museo del Prado', 'precio': 15, 'duracion': '2 horas', 'horario': '10:00-20:00'},
                {'nombre': 'Tour por el Santiago Bernabéu', 'precio': 25, 'duracion': '1.5 horas', 'horario': '9:30-19:00'},
                {'nombre': 'Paseo por el Parque del Retiro', 'precio': 0, 'duracion': 'libre', 'horario': '24h'},
                {'nombre': 'Tapas en La Latina', 'precio': 30, 'duracion': '3 horas', 'horario': '19:00-23:00'}
            ],
            'París': [
                {'nombre': 'Tour por la Torre Eiffel', 'precio': 40, 'duracion': '2 horas', 'horario': '9:00-22:00'},
                {'nombre': 'Visita al Museo del Louvre', 'precio': 35, 'duracion': '3 horas', 'horario': '9:00-18:00'},
                {'nombre': 'Paseo en barco por el Sena', 'precio': 25, 'duracion': '1 hora', 'horario': '10:00-22:00'},
                {'nombre': 'Tour de compras en Champs-Élysées', 'precio': 20, 'duracion': '2 horas', 'horario': '10:00-19:00'}
            ]
        }

        # Agregar patrones de respuestas afirmativas/negativas más completos
        self.respuestas_simples = {
            'afirmativo': r'(?i)(^si$|^sí$|^ok$|^dale$|^bueno$|^claro$|^por supuesto$|^me gustaría$|'
                         r'^vale$|^va$|^venga$|^está bien$|^correcto$|^adelante$|'
                         r'^si.*por favor$|^si.*gracias$|^si.*claro$|'
                         r'^me parece bien$|^me interesa$|^quiero$)',
            
            'negativo': r'(?i)(^no$|^nop$|^nel$|^paso$|^mejor no$|^negativo$|'
                       r'^no.*gracias$|^no.*por ahora$|^ahora no$|'
                       r'^en otro momento$|^quizás luego$|^más tarde$)',
            
            'gracias': r'(?i)(^gracias$|^muchas gracias$|^genial$|^excelente$|^perfecto$|'
                      r'^gracias.*ayuda$|^muy amable$|^te lo agradezco$)',
            
            'duda': r'(?i)(^no.*seguro$|^quizás$|^tal vez$|^puede ser$|'
                    r'^depende$|^lo pensaré$|^necesito pensarlo$)',
            
            'consulta_precio': r'(?i)(^cuánto.*cuesta.*$|^qué precio.*$|^precio.*$)',
            
            'consulta_tiempo': r'(?i)(^cuánto.*tarda.*$|^duración.*$|^tiempo.*viaje.*$)'
        }

        # Respuestas para cada tipo
        self.respuestas_por_tipo = {
            'duda': [
                "Tómate tu tiempo para decidir. ¿Te gustaría más información sobre algo en particular?",
                "Entiendo. ¿Hay algo específico que te preocupe?",
                "¿Qué información adicional necesitas para decidir?"
            ],
            'consulta_precio': [
                "¿Para qué destino te gustaría saber los precios?",
                "Puedo ayudarte con los precios. ¿Qué destino te interesa?",
                "Dime el destino y te muestro los precios disponibles"
            ],
            'consulta_tiempo': [
                "¿Para qué destino quieres saber la duración del viaje?",
                "¿A qué destino te gustaría viajar? Te diré la duración",
                "Dime el destino y te informo sobre los tiempos de viaje"
            ]
        }
        
        # Agregar estado de conversación
        self.contexto = {
            'ultimo_destino': None,
            'ultima_accion': None,
            'esperando_confirmacion': False,
            'siguiente_accion': None
        }

        # Agregar patrones para preguntas generales
        self.patrones_ayuda = {
            'que_mas': r'(?i)(^qué más.*$|^que mas.*$|^qué otra cosa.*$|^qué más puedo.*$|'
                      r'^qué puedo.*$|^que puedo.*$|^qué me.*ofreces.*$|^qué.*hacer.*$)',
            
            'ayuda': r'(?i)(^ayuda.*$|^help.*$|^necesito ayuda.*$|^cómo.*funciona.*$|'
                    r'^qué.*puedes hacer.*$|^cuáles.*opciones.*$|^menu.*$|^opciones.*$)',
            
            'servicios': r'(?i)(^servicios.*$|^qué.*servicios.*$|^que.*ofreces.*$|'
                        r'^con qué.*ayudas.*$|^qué.*consultar.*$)'
        }
        
        # Mensajes de ayuda
        self.mensajes_ayuda = {
            'general': [
                """Puedo ayudarte con:
1. Búsqueda de vuelos a diferentes destinos
2. Información de hoteles y alojamiento
3. Actividades turísticas y atracciones
4. Precios y duración de viajes
5. Preferencias de viaje (asiento, clase)

¿Sobre qué te gustaría consultar?""",
                """Estos son mis servicios principales:
- Búsqueda de vuelos
- Reservas de hoteles
- Información turística
- Consulta de precios
- Gestión de preferencias

¿En qué puedo ayudarte?"""
            ],
            'ejemplos': [
                """Aquí tienes algunos ejemplos de lo que puedes preguntarme:
- "Busco vuelos a Madrid"
- "Hoteles en París"
- "Qué se puede hacer en Roma"
- "Prefiero asiento ventana"
- "Cuánto cuesta ir a Londres"

¿Qué te gustaría consultar?"""
            ]
        }

        # Sistema de intenciones y entidades
        self.intenciones = {
            'buscar_vuelo': {
                'patrones': [
                    r'(?i).*(?:vuelo|volar|viaje).*(?:a|hacia|para) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:ir|viajar).*(?:a|hacia) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:quiero|necesito).*(?:ir|viajar|volar).*(?:a|hacia) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i)^(?:buscar?|reservar?|quiero?)?\s*(?:vuelo|vuelos?)(?:\s+(?:a|hacia|para)\s+)?([A-Za-zÁ-úñÑ\s]+)?$'
                ],
                'entidades_requeridas': ['destino'],
                'respuesta_faltantes': "¿A qué destino te gustaría viajar? Tenemos vuelos a: Madrid, Barcelona, París, Londres, Roma, Berlín, Ámsterdam y Lisboa"
            },
            'buscar_hotel': {
                'patrones': [
                    r'(?i).*(?:hotel|alojamiento|hospedaje).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:dormir|quedarme).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:busco|necesito).*(?:hotel|alojamiento).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:reservar|hacer reserva|hacer una reserva).*(?:hotel|alojamiento)(?:\sen\s)?([A-Za-zÁ-úñÑ\s]+)?',
                    r'(?i)^(?:hotel|hoteles|alojamiento)(?:\sen\s)?([A-Za-zÁ-úñÑ\s]+)?$',
                    r'(?i).*(?:quiero|necesito).*(?:reservar|hotel|alojamiento)(?:\sen\s)?([A-Za-zÁ-úñÑ\s]+)?'
                ],
                'entidades_requeridas': ['destino'],
                'respuesta_faltantes': "¿En qué ciudad buscas alojamiento?"
            },
            'consultar_actividades': {
                'patrones': [
                    r'(?i).*(?:hacer|actividades|turismo).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:visitar|conocer).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:qué hay|qué ver).*(?:en) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:información|info).*(?:turística|turismo).*(?:en) ([A-Za-zÁ-úñÑ\s]+)?'
                ],
                'entidades_requeridas': ['destino'],
                'respuesta_faltantes': "¿De qué ciudad te gustaría conocer las actividades?"
            },
            'cambiar_preferencias': {
                'patrones': [
                    r'(?i).*(?:prefiero|quiero|cambiar a) (ventana|pasillo|business|económica)',
                    r'(?i).*(?:asiento|clase) (ventana|pasillo|business|económica)',
                    r'(?i).*(?:cambiar|modificar).*(?:asiento|clase) (?:a|por) (ventana|pasillo|business|económica)'
                ],
                'entidades_requeridas': ['preferencia'],
                'respuesta_faltantes': "¿Qué preferencia te gustaría modificar?"
            },
            'consultar_precio': {
                'patrones': [
                    r'(?i).*(?:precio|costo|valor).*(?:a|de|para) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:cuánto|cuanto).*(?:cuesta|vale).*(?:a|para) ([A-Za-zÁ-úñÑ\s]+)',
                    r'(?i).*(?:precio|costo).*(?:del viaje|del vuelo).*(?:a) ([A-Za-zÁ-úñÑ\s]+)'
                ],
                'entidades_requeridas': ['destino'],
                'respuesta_faltantes': "¿Para qué destino quieres consultar el precio?"
            }
        }

        # Estado de la conversación
        self.estado_conversacion = {
            'intencion_actual': None,
            'entidades_detectadas': {},
            'entidades_faltantes': [],
            'contexto_anterior': None,
            'esperando_entidad': False
        }

        # Mapa de normalización de ciudades
        self.normalizacion_ciudades = {
            'madrid': 'Madrid',
            'barcelona': 'Barcelona',
            'paris': 'París',
            'londres': 'Londres',
            'roma': 'Roma',
            'berlin': 'Berlín',
            'amsterdam': 'Ámsterdam',
            'lisboa': 'Lisboa',
            # Variaciones comunes
            'bcn': 'Barcelona',
            'barna': 'Barcelona',
            'mad': 'Madrid',
            'paris': 'París',
            'london': 'Londres',
            'rome': 'Roma',
            'berlin': 'Berlín',
            'amsterdam': 'Ámsterdam',
            'lisbon': 'Lisboa'
        }

        # Agregar estado de reserva
        self.reserva_actual = {
            'hotel': None,
            'fechas': None,
            'habitaciones': None,
            'precio_total': None,
            'numero_reserva': None
        }

        # Agregar estados de reserva combinados (hotel y vuelo)
        self.estados_reserva = {
            # Estados de reserva de hotel
            'seleccionar_hotel': self.seleccionar_hotel,
            'pedir_fechas': self.pedir_fechas,
            'pedir_habitaciones': self.pedir_habitaciones,
            'confirmar_reserva': self.confirmar_reserva,
            'procesar_pago': self.procesar_pago,
            'finalizar_reserva': self.finalizar_reserva,
            
            # Estados de reserva de vuelo
            'seleccionar_fecha_vuelo': self.seleccionar_fecha_vuelo,
            'seleccionar_pasajeros': self.seleccionar_pasajeros,
            'confirmar_vuelo': self.confirmar_vuelo,
            'procesar_pago_vuelo': self.procesar_pago_vuelo,
            'finalizar_reserva_vuelo': self.finalizar_reserva_vuelo
        }

        # Agregar estado de reserva de vuelo
        self.reserva_vuelo = {
            'vuelo': None,
            'fecha': None,
            'pasajeros': None,
            'precio_total': None,
            'numero_reserva': None,
            'destino': None
        }

        # Agregar estado de reserva de actividad
        self.reserva_actividad = {
            'actividad': None,
            'fecha': None,
            'hora': None,
            'personas': None,
            'precio_total': None,
            'numero_reserva': None
        }

        # Añadir estados de reserva de actividad
        self.estados_reserva.update({
            'seleccionar_actividad': self.seleccionar_actividad,
            'seleccionar_fecha_actividad': self.seleccionar_fecha_actividad,
            'seleccionar_hora': self.seleccionar_hora,
            'seleccionar_personas_actividad': self.seleccionar_personas_actividad,
            'confirmar_actividad': self.confirmar_actividad,
            'procesar_pago_actividad': self.procesar_pago_actividad,
            'finalizar_reserva_actividad': self.finalizar_reserva_actividad
        })

    def detectar_intencion_y_entidades(self, texto):
        """Detecta la intención y entidades en el texto del usuario"""
        for intencion, config in self.intenciones.items():
            for patron in config['patrones']:
                match = re.match(patron, texto)
                if match:
                    entidades = {}
                    if len(match.groups()) > 0:
                        # La primera entidad suele ser el destino o la preferencia
                        entidad_valor = match.group(1).strip().title() if match.group(1) else None
                        entidad_tipo = 'destino' if intencion != 'cambiar_preferencias' else 'preferencia'
                        if entidad_valor:
                            entidades[entidad_tipo] = entidad_valor
                    
                    return {
                        'intencion': intencion,
                        'entidades': entidades,
                        'texto_original': texto
                    }
        
        return None

    def procesar_entrada(self, texto):
        """Procesa la entrada del usuario usando el sistema de intenciones"""
        # Verificar si estamos en un estado de reserva
        if 'siguiente_estado' in self.estado_conversacion and self.estado_conversacion['siguiente_estado']:
            estado = self.estado_conversacion['siguiente_estado']
            return self.estados_reserva[estado](texto)
        
        # Verificar si estamos esperando una entidad específica
        if self.estado_conversacion['esperando_entidad']:
            return self.manejar_respuesta_entidad(texto)
        
        # Detectar intención y entidades
        resultado = self.detectar_intencion_y_entidades(texto)
        if resultado:
            return self.manejar_intencion_detectada(resultado)
        
        # Verificar patrones simples de intención sin destino
        texto_lower = texto.lower().strip()
        if any(palabra in texto_lower for palabra in ['vuelo', 'volar', 'viaje', 'vuelos']):
            return self.intenciones['buscar_vuelo']['respuesta_faltantes']
        
        # Si no se detecta intención, verificar respuestas simples
        for tipo, patron in self.respuestas_simples.items():
            if re.match(patron, texto):
                return self.manejar_respuesta_simple(tipo)
        
        # Si nada coincide, mostrar ayuda
        return self.mostrar_ayuda('general')

    def manejar_intencion_detectada(self, resultado):
        """Maneja una intención detectada y sus entidades"""
        intencion = resultado['intencion']
        entidades = resultado['entidades']
        config_intencion = self.intenciones[intencion]
        
        # Verificar si tenemos todas las entidades requeridas
        entidades_faltantes = [
            entidad for entidad in config_intencion['entidades_requeridas']
            if entidad not in entidades
        ]
        
        if entidades_faltantes:
            # Guardar estado para esperar la respuesta
            self.estado_conversacion['intencion_actual'] = intencion
            self.estado_conversacion['entidades_detectadas'] = entidades
            self.estado_conversacion['entidades_faltantes'] = entidades_faltantes
            self.estado_conversacion['esperando_entidad'] = True
            
            return config_intencion['respuesta_faltantes']
        
        # Si tenemos todas las entidades, procesar la intención
        return self.ejecutar_intencion(intencion, entidades)

    def manejar_respuesta_entidad(self, texto):
        """Maneja la respuesta cuando estamos esperando una entidad"""
        entidad_faltante = self.estado_conversacion['entidades_faltantes'][0]
        
        # Limpiar y validar la entrada
        valor = texto.strip()
        if self.validar_entidad(entidad_faltante, valor):
            # Normalizar el valor si es una ciudad
            if entidad_faltante == 'destino':
                valor = self.normalizar_ciudad(valor)
            
            # Agregar la entidad y procesar
            self.estado_conversacion['entidades_detectadas'][entidad_faltante] = valor
            self.estado_conversacion['entidades_faltantes'].pop(0)
            self.estado_conversacion['esperando_entidad'] = False
            
            return self.ejecutar_intencion(
                self.estado_conversacion['intencion_actual'],
                self.estado_conversacion['entidades_detectadas']
            )
        
        return f"Lo siento, no tengo información para {valor}. Por favor, elige entre: {', '.join(sorted(set(self.normalizacion_ciudades.values())))}."

    def ejecutar_intencion(self, intencion, entidades):
        """Ejecuta una intención con sus entidades completas"""
        if intencion == 'buscar_vuelo':
            return self.buscar_vuelos(entidades['destino'])
        elif intencion == 'buscar_hotel':
            return self.buscar_hoteles(entidades['destino'])
        elif intencion == 'consultar_actividades':
            return self.sugerir_actividades(entidades['destino'])
        elif intencion == 'cambiar_preferencias':
            return self.actualizar_preferencias(entidades['preferencia'])
        elif intencion == 'consultar_precio':
            return self.consultar_precios(entidades['destino'])

    def validar_entidad(self, tipo_entidad, valor):
        """Valida una entidad según su tipo con mejor manejo de casos"""
        if tipo_entidad == 'destino':
            # Normalizar el nombre de la ciudad
            valor_normalizado = self.normalizar_ciudad(valor)
            if valor_normalizado:
                return True
            return False
        elif tipo_entidad == 'preferencia':
            return valor.lower() in ['ventana', 'pasillo', 'business', 'económica']
        return False

    def normalizar_ciudad(self, ciudad):
        """Normaliza el nombre de una ciudad"""
        ciudad_lower = ciudad.lower()
        if ciudad_lower in self.normalizacion_ciudades:
            return self.normalizacion_ciudades[ciudad_lower]
        return None

    def mostrar_ayuda(self, tipo):
        """Muestra mensajes de ayuda según el tipo de consulta"""
        if tipo in ['que_mas', 'ayuda', 'servicios']:
            # Alternar entre mensajes generales y ejemplos
            if random.random() < 0.5:
                return random.choice(self.mensajes_ayuda['general'])
            else:
                return random.choice(self.mensajes_ayuda['ejemplos'])
        
        return random.choice(self.mensajes_ayuda['general'])

    def manejar_respuesta_simple(self, tipo):
        """Maneja respuestas simples fuera de contexto"""
        if tipo == 'gracias':
            return random.choice([
                "¡De nada! ¿Hay algo más en lo que pueda ayudarte?",
                "Es un placer ayudarte. ¿Necesitas algo más?",
                "Para eso estoy. ¿Puedo ayudarte con algo más?"
            ])
        
        if tipo in self.respuestas_por_tipo:
            return random.choice(self.respuestas_por_tipo[tipo])
        
        # Si no hay respuesta específica, mostrar ayuda general
        return self.mostrar_ayuda('general')

    def buscar_vuelos(self, destino):
        """Simula búsqueda de vuelos en tiempo real"""
        if destino not in self.vuelos_disponibles:
            return f"Lo siento, no tenemos vuelos disponibles a {destino}."
        
        # Simular demora de búsqueda en APIs
        time.sleep(1.5)
        
        vuelo = self.vuelos_disponibles[destino]
        clase = self.preferencias_usuario['clase']
        precio = vuelo['precio'][clase]
        
        # Guardar información del vuelo
        self.reserva_vuelo = {
            'vuelo': vuelo,
            'destino': destino,
            'clase': clase,
            'precio_base': precio
        }
        
        # Cambiar a estado de reserva de vuelo
        self.estado_conversacion['siguiente_estado'] = 'seleccionar_fecha_vuelo'
        
        return f"""He encontrado vuelos a {destino}:
- Clase {clase}
- Precio: ${precio} por persona
- Duración: {vuelo['duracion']}
- Escalas: {vuelo['escalas']}
- Asiento: {self.preferencias_usuario['asiento']}

¿Para qué fecha desea viajar? (formato: DD/MM/YYYY)"""

    def seleccionar_fecha_vuelo(self, fecha):
        """Procesa la selección de fecha del vuelo"""
        try:
            # Aquí podrías añadir validación de fecha
            self.reserva_vuelo['fecha'] = fecha
            self.estado_conversacion['siguiente_estado'] = 'seleccionar_pasajeros'
            return "¿Cuántos pasajeros viajarán? (1-6)"
        except:
            return "Por favor, ingrese la fecha en el formato correcto (DD/MM/YYYY)"

    def seleccionar_pasajeros(self, cantidad):
        """Procesa la cantidad de pasajeros"""
        try:
            num_pasajeros = int(cantidad)
            if 1 <= num_pasajeros <= 6:
                self.reserva_vuelo['pasajeros'] = num_pasajeros
                self.reserva_vuelo['precio_total'] = self.reserva_vuelo['precio_base'] * num_pasajeros
                return self.mostrar_resumen_vuelo()
            else:
                return "Por favor, seleccione entre 1 y 6 pasajeros."
        except ValueError:
            return "Por favor, ingrese un número válido de pasajeros."

    def mostrar_resumen_vuelo(self):
        """Muestra el resumen de la reserva de vuelo"""
        resumen = f"\nResumen de su vuelo:\n"
        resumen += f"Destino: {self.reserva_vuelo['destino']}\n"
        resumen += f"Fecha: {self.reserva_vuelo['fecha']}\n"
        resumen += f"Pasajeros: {self.reserva_vuelo['pasajeros']}\n"
        resumen += f"Clase: {self.reserva_vuelo['clase']}\n"
        resumen += f"Asiento: {self.preferencias_usuario['asiento']}\n"
        resumen += f"Precio por persona: ${self.reserva_vuelo['precio_base']}\n"
        resumen += f"Precio total: ${self.reserva_vuelo['precio_total']}\n"
        resumen += f"Duración: {self.reserva_vuelo['vuelo']['duracion']}\n"
        resumen += f"Escalas: {self.reserva_vuelo['vuelo']['escalas']}\n\n"
        resumen += "¿Desea confirmar la reserva del vuelo? (si/no)"
        
        self.estado_conversacion['siguiente_estado'] = 'confirmar_vuelo'
        return resumen

    def confirmar_vuelo(self, confirmacion):
        """Procesa la confirmación del vuelo"""
        if confirmacion.lower() in ['si', 'sí', 'confirmar']:
            self.estado_conversacion['siguiente_estado'] = 'procesar_pago_vuelo'
            return "Perfecto. Procesando su reserva de vuelo...\n¿Cómo desea realizar el pago? (1: Tarjeta de crédito, 2: PayPal)"
        elif confirmacion.lower() in ['no', 'cancelar']:
            self.reserva_vuelo = {}
            return "Reserva de vuelo cancelada. ¿Puedo ayudarle con algo más?"
        else:
            return "Por favor, responda 'si' o 'no'."

    def procesar_pago_vuelo(self, metodo_pago):
        """Simula el procesamiento del pago del vuelo"""
        try:
            metodo = int(metodo_pago)
            if metodo in [1, 2]:
                time.sleep(2)  # Simular procesamiento
                self.reserva_vuelo['numero_reserva'] = f"VUE-{random.randint(10000, 99999)}"
                return self.finalizar_reserva_vuelo()
            else:
                return "Por favor, seleccione 1 para tarjeta de crédito o 2 para PayPal."
        except ValueError:
            return "Por favor, seleccione una opción válida."

    def finalizar_reserva_vuelo(self, _=None):
        """Finaliza el proceso de reserva de vuelo"""
        confirmacion = f"""¡Reserva de vuelo confirmada!
Número de reserva: {self.reserva_vuelo['numero_reserva']}
Destino: {self.reserva_vuelo['destino']}
Fecha: {self.reserva_vuelo['fecha']}
Pasajeros: {self.reserva_vuelo['pasajeros']}
Clase: {self.reserva_vuelo['clase']}
Precio total: ${self.reserva_vuelo['precio_total']}

Recibirá un email con los detalles de su vuelo y la tarjeta de embarque.
¿Le gustaría buscar un hotel en {self.reserva_vuelo['destino']}?"""
        
        # Guardar destino para posible reserva de hotel
        self.estado_conversacion['destino_pendiente'] = self.reserva_vuelo['destino']
        self.estado_conversacion['esperando_confirmacion_hotel'] = True
        
        # Limpiar estado de reserva de vuelo pero mantener el contexto para hotel
        self.reserva_vuelo = {}
        self.estado_conversacion['siguiente_estado'] = None
        
        return confirmacion

    def buscar_hoteles(self, destino):
        """Simula búsqueda de hoteles según preferencias"""
        if destino not in self.hoteles_disponibles:
            return f"Lo siento, no tengo información de hoteles en {destino}."
        
        # Simular demora de búsqueda
        time.sleep(1)
        
        estrellas_preferidas = int(self.preferencias_usuario['tipo_hotel'].split()[0])
        hoteles = self.hoteles_disponibles[destino]
        
        # Filtrar por preferencias
        hoteles_sugeridos = [h for h in hoteles if abs(h['estrellas'] - estrellas_preferidas) <= 1]
        
        if not hoteles_sugeridos:
            hoteles_sugeridos = hoteles

        # Guardar hoteles para la selección
        self.reserva_actual['destino'] = destino
        self.reserva_actual['hoteles_disponibles'] = hoteles_sugeridos
        
        respuesta = f"He encontrado estos hoteles en {destino} según tus preferencias:\n"
        for i, hotel in enumerate(hoteles_sugeridos, 1):
            respuesta += f"{i}. {hotel['nombre']}: {hotel['estrellas']}⭐ - ${hotel['precio']}/noche\n"
        
        respuesta += "\nPor favor, seleccione el número del hotel que le interesa (o 'cancelar' para salir)"
        
        # Cambiar a estado de reserva
        self.estado_conversacion['siguiente_estado'] = 'seleccionar_hotel'
        self.estado_conversacion['esperando_entidad'] = False  # Ya no usamos el sistema de entidades
        
        return respuesta

    def seleccionar_hotel(self, seleccion):
        """Procesa la selección del hotel"""
        try:
            if seleccion.lower() == 'cancelar':
                self.estado_conversacion['esperando_entidad'] = False
                return "Reserva cancelada. ¿Puedo ayudarte con algo más?"

            indice = int(seleccion) - 1
            hoteles = self.reserva_actual['hoteles_disponibles']
            if 0 <= indice < len(hoteles):
                self.reserva_actual['hotel'] = hoteles[indice]
                self.estado_conversacion['siguiente_estado'] = 'pedir_fechas'
                return "¿Para qué fechas desea hacer la reserva? (formato: DD/MM/YYYY - DD/MM/YYYY)"
            else:
                return "Por favor, seleccione un número válido de hotel."
        except ValueError:
            return "Por favor, ingrese un número válido o 'cancelar'."

    def pedir_fechas(self, fechas):
        """Procesa las fechas de la reserva"""
        try:
            inicio, fin = fechas.split(' - ')
            # Aquí podrías añadir validación de fechas
            self.reserva_actual['fechas'] = {'inicio': inicio, 'fin': fin}
            self.estado_conversacion['siguiente_estado'] = 'pedir_habitaciones'
            return "¿Cuántas habitaciones desea reservar? (1-5)"
        except:
            return "Por favor, ingrese las fechas en el formato correcto (DD/MM/YYYY - DD/MM/YYYY)"

    def pedir_habitaciones(self, cantidad):
        """Procesa la cantidad de habitaciones"""
        try:
            num_habitaciones = int(cantidad)
            if 1 <= num_habitaciones <= 5:
                self.reserva_actual['habitaciones'] = num_habitaciones
                precio_noche = self.reserva_actual['hotel']['precio']
                self.reserva_actual['precio_total'] = precio_noche * num_habitaciones
                return self.mostrar_resumen_reserva()
            else:
                return "Por favor, seleccione entre 1 y 5 habitaciones."
        except ValueError:
            return "Por favor, ingrese un número válido de habitaciones."

    def mostrar_resumen_reserva(self):
        """Muestra el resumen de la reserva"""
        hotel = self.reserva_actual['hotel']
        resumen = f"\nResumen de su reserva:\n"
        resumen += f"Hotel: {hotel['nombre']} ({hotel['estrellas']}⭐)\n"
        resumen += f"Fechas: {self.reserva_actual['fechas']['inicio']} - {self.reserva_actual['fechas']['fin']}\n"
        resumen += f"Habitaciones: {self.reserva_actual['habitaciones']}\n"
        resumen += f"Precio por noche: ${hotel['precio']}\n"
        resumen += f"Precio total: ${self.reserva_actual['precio_total']}\n\n"
        resumen += "¿Desea confirmar la reserva? (si/no)"
        
        self.estado_conversacion['siguiente_estado'] = 'confirmar_reserva'
        return resumen

    def confirmar_reserva(self, confirmacion):
        """Procesa la confirmación de la reserva"""
        if confirmacion.lower() in ['si', 'sí', 'confirmar']:
            self.estado_conversacion['siguiente_estado'] = 'procesar_pago'
            return "Perfecto. Procesando su reserva...\n¿Cómo desea realizar el pago? (1: Tarjeta de crédito, 2: PayPal)"
        elif confirmacion.lower() in ['no', 'cancelar']:
            self.reserva_actual = {}
            return "Reserva cancelada. ¿Puedo ayudarle con algo más?"
        else:
            return "Por favor, responda 'si' o 'no'."

    def procesar_pago(self, metodo_pago):
        """Simula el procesamiento del pago"""
        try:
            metodo = int(metodo_pago)
            if metodo in [1, 2]:
                time.sleep(2)  # Simular procesamiento
                self.reserva_actual['numero_reserva'] = f"RES-{random.randint(10000, 99999)}"
                return self.finalizar_reserva()
            else:
                return "Por favor, seleccione 1 para tarjeta de crédito o 2 para PayPal."
        except ValueError:
            return "Por favor, seleccione una opción válida."

    def finalizar_reserva(self, _=None):
        """Finaliza el proceso de reserva"""
        confirmacion = f"""¡Reserva confirmada!
Número de reserva: {self.reserva_actual['numero_reserva']}
Hotel: {self.reserva_actual['hotel']['nombre']}
Fechas: {self.reserva_actual['fechas']['inicio']} - {self.reserva_actual['fechas']['fin']}
Habitaciones: {self.reserva_actual['habitaciones']}
Precio total: ${self.reserva_actual['precio_total']}

Recibirá un email con los detalles de su reserva.
¿Puedo ayudarle con algo más?"""
        
        # Limpiar estado de reserva
        self.reserva_actual = {}
        self.estado_conversacion['esperando_entidad'] = False
        self.estado_conversacion['siguiente_estado'] = None
        
        return confirmacion

    def sugerir_actividades(self, destino):
        """Sugiere actividades basadas en el destino"""
        if destino not in self.actividades:
            return f"Lo siento, no tengo información de actividades en {destino}."
        
        # Guardar destino para la reserva
        self.reserva_actividad['destino'] = destino
        self.reserva_actividad['actividades_disponibles'] = self.actividades[destino]
        
        respuesta = f"Actividades disponibles en {destino}:\n"
        for i, actividad in enumerate(self.actividades[destino], 1):
            respuesta += f"{i}. {actividad['nombre']}\n"
            respuesta += f"   Precio: ${actividad['precio']} - Duración: {actividad['duracion']}\n"
            respuesta += f"   Horario: {actividad['horario']}\n"
        
        respuesta += "\n¿Le gustaría reservar alguna actividad? Seleccione el número o escriba 'no'"
        self.estado_conversacion['siguiente_estado'] = 'seleccionar_actividad'
        return respuesta

    def seleccionar_actividad(self, seleccion):
        """Procesa la selección de actividad"""
        if seleccion.lower() == 'no':
            self.estado_conversacion['siguiente_estado'] = None
            return "De acuerdo. ¿Hay algo más en lo que pueda ayudarte?"
            
        try:
            indice = int(seleccion) - 1
            actividades = self.reserva_actividad['actividades_disponibles']
            if 0 <= indice < len(actividades):
                self.reserva_actividad['actividad'] = actividades[indice]
                self.estado_conversacion['siguiente_estado'] = 'seleccionar_fecha_actividad'
                return "¿Para qué fecha desea reservar la actividad? (formato: DD/MM/YYYY)"
            else:
                return "Por favor, seleccione un número válido de actividad."
        except ValueError:
            return "Por favor, ingrese un número válido o 'no'."

    def seleccionar_fecha_actividad(self, fecha):
        """Procesa la fecha para la actividad"""
        try:
            # Aquí podrías validar la fecha
            self.reserva_actividad['fecha'] = fecha
            self.estado_conversacion['siguiente_estado'] = 'seleccionar_hora'
            return f"¿A qué hora desea realizar la actividad? (Horario disponible: {self.reserva_actividad['actividad']['horario']})"
        except:
            return "Por favor, ingrese la fecha en el formato correcto (DD/MM/YYYY)"

    def seleccionar_hora(self, hora):
        """Procesa la hora seleccionada"""
        # Aquí podrías validar la hora
        self.reserva_actividad['hora'] = hora
        self.estado_conversacion['siguiente_estado'] = 'seleccionar_personas_actividad'
        return "¿Cuántas personas participarán en la actividad? (1-10)"

    def seleccionar_personas_actividad(self, cantidad):
        """Procesa la cantidad de personas"""
        try:
            num_personas = int(cantidad)
            if 1 <= num_personas <= 10:
                self.reserva_actividad['personas'] = num_personas
                self.reserva_actividad['precio_total'] = self.reserva_actividad['actividad']['precio'] * num_personas
                return self.mostrar_resumen_actividad()
            else:
                return "Por favor, seleccione entre 1 y 10 personas."
        except ValueError:
            return "Por favor, ingrese un número válido de personas."

    def mostrar_resumen_actividad(self):
        """Muestra el resumen de la reserva de actividad"""
        actividad = self.reserva_actividad['actividad']
        resumen = f"\nResumen de su reserva de actividad:\n"
        resumen += f"Actividad: {actividad['nombre']}\n"
        resumen += f"Fecha: {self.reserva_actividad['fecha']}\n"
        resumen += f"Hora: {self.reserva_actividad['hora']}\n"
        resumen += f"Personas: {self.reserva_actividad['personas']}\n"
        resumen += f"Precio por persona: ${actividad['precio']}\n"
        resumen += f"Precio total: ${self.reserva_actividad['precio_total']}\n"
        resumen += f"Duración: {actividad['duracion']}\n\n"
        resumen += "¿Desea confirmar la reserva de la actividad? (si/no)"
        
        self.estado_conversacion['siguiente_estado'] = 'confirmar_actividad'
        return resumen

    def confirmar_actividad(self, confirmacion):
        """Procesa la confirmación de la actividad"""
        if confirmacion.lower() in ['si', 'sí', 'confirmar']:
            self.estado_conversacion['siguiente_estado'] = 'procesar_pago_actividad'
            return "Perfecto. Procesando su reserva...\n¿Cómo desea realizar el pago? (1: Tarjeta de crédito, 2: PayPal)"
        elif confirmacion.lower() in ['no', 'cancelar']:
            self.reserva_actividad = {}
            return "Reserva cancelada. ¿Puedo ayudarle con algo más?"
        else:
            return "Por favor, responda 'si' o 'no'."

    def procesar_pago_actividad(self, metodo_pago):
        """Simula el procesamiento del pago de la actividad"""
        try:
            metodo = int(metodo_pago)
            if metodo in [1, 2]:
                time.sleep(2)  # Simular procesamiento
                self.reserva_actividad['numero_reserva'] = f"ACT-{random.randint(10000, 99999)}"
                return self.finalizar_reserva_actividad()
            else:
                return "Por favor, seleccione 1 para tarjeta de crédito o 2 para PayPal."
        except ValueError:
            return "Por favor, seleccione una opción válida."

    def finalizar_reserva_actividad(self, _=None):
        """Finaliza el proceso de reserva de actividad"""
        confirmacion = f"""¡Reserva de actividad confirmada!
Número de reserva: {self.reserva_actividad['numero_reserva']}
Actividad: {self.reserva_actividad['actividad']['nombre']}
Fecha: {self.reserva_actividad['fecha']}
Hora: {self.reserva_actividad['hora']}
Personas: {self.reserva_actividad['personas']}
Precio total: ${self.reserva_actividad['precio_total']}

Recibirá un email con los detalles de su reserva y los tickets.
¿Puedo ayudarle con algo más?"""
        
        # Limpiar estado de reserva
        self.reserva_actividad = {}
        self.estado_conversacion['siguiente_estado'] = None
        
        return confirmacion

    def actualizar_preferencias(self, preferencia):
        """Actualiza preferencias del usuario"""
        if preferencia in ['ventana', 'pasillo']:
            self.preferencias_usuario['asiento'] = preferencia
        elif preferencia in ['business', 'económica']:
            self.preferencias_usuario['clase'] = preferencia
        
        return f"He actualizado tus preferencias. Ahora buscaré opciones con asiento en {preferencia}."

def main():
    print("\n" + "*" * 78)
    print("*  TravelPal - Tu Asistente Virtual de Viajes")
    print("*  Puedo ayudarte a buscar vuelos, hoteles y planificar actividades")
    print("*" + "*" * 71)
    
    print("""\nPuedo entender las siguientes consultas:

1. Búsqueda de Vuelos:
   - "Busco vuelos a Madrid"
   - "Quiero viajar a París"
   - "Necesito ir a Roma"

2. Búsqueda de Hoteles:
   - "Hoteles en Madrid"
   - "Busco alojamiento en París"
   - "Quiero reservar hotel en Roma"

3. Consulta de Actividades:
   - "Qué se puede hacer en Madrid"
   - "Actividades en París"
   - "Qué hay para visitar en Roma"

4. Preferencias de Viaje:
   - "Prefiero asiento ventana"
   - "Quiero viajar en business"
   - "Cambiar a asiento pasillo"

5. Consulta de Precios:
   - "Cuánto cuesta ir a Madrid"
   - "Precio de vuelos a París"
   - "Valor del viaje a Roma"

También puedes preguntarme:
- "Qué más puedes hacer"
- "Necesito ayuda"
- "Muestra opciones"
""")
    
    asistente = TravelPal()
    print("\nTravelPal: ¡Hola! Soy tu asistente de viajes. ¿En qué puedo ayudarte?")
    print("          Puedes preguntarme sobre cualquiera de las opciones anteriores.")
    
    while True:
        entrada = input("\nTú: ").strip()
        
        if entrada.lower() in ['salir', 'adiós', 'adios', 'chau']:
            print("\nTravelPal: ¡Que tengas un excelente viaje! ¡Hasta pronto!")
            break
            
        respuesta = asistente.procesar_entrada(entrada)
        print(f"\nTravelPal: {respuesta}")

if __name__ == "__main__":
    main() 