import re
import random
import time

class Parry:
    def __init__(self):
        # Estados base más alineados con paranoia
        self.desconfianza = 15  # Nivel base alto de desconfianza
        self.miedo = 10        # Ansiedad moderada-alta
        self.enojo = 8         # Irritabilidad moderada
        
        # Creencias delirantes centrales
        self.creencias_core = {
            'persecución': "La mafia del hipódromo me persigue desde que descubrí sus secretos",
            'conspiración': "Los médicos y la policía trabajan juntos para encubrir todo",
            'vigilancia': "Me vigilan constantemente, tienen espías en todas partes",
            'control': "Usan las carreras de caballos para controlar las mentes de la gente",
            'traición': "Mi propia familia está involucrada, aunque no lo saben",
            'drogas': "Ponen sustancias en el agua para controlarnos mejor",
            'tecnología': "Usan satélites para rastrear todos mis movimientos",
            'gobierno': "El gobierno tiene una base secreta bajo el hipódromo",
            'experimentos': "Hacen experimentos con la gente en los hospitales",
            'infiltrados': "Hay infiltrados en todos lados, incluso entre los pacientes"
        }
        
        # Patrones de pensamiento paranoide
        self.patrones_pensamiento = {
            'interrogatorio': [
                "¿Por qué hace tantas preguntas? ¿Quién lo envía?",
                "¿Está tomando notas? ¿Para quién son?",
                "¿Cómo sé que puedo confiar en usted?",
                "Esas preguntas parecen sospechosas... ¿qué busca realmente?",
                "¿Le han dicho que me pregunte específicamente sobre esto?",
                "¿Está grabando esta conversación?",
                "¿Por qué tanto interés en mis asuntos?",
                "¿Quién más sabe que estoy aquí?"
            ],
            'amenaza': [
                "No debería estar hablando de esto aquí...",
                "*Mirando nerviosamente a su alrededor* Nos pueden estar escuchando",
                "Tienen micrófonos en todas partes, ¿sabe?",
                "No es seguro discutir estos temas",
                "*Susurrando* Las paredes tienen oídos...",
                "Están vigilando cada movimiento que hacemos",
                "Podrían estar observándonos ahora mismo",
                "He visto cámaras ocultas en las ventilaciones"
            ],
            'desconfianza': [
                "¿Está seguro que es doctor? Muéstreme sus credenciales",
                "He visto cómo miran los 'doctores', todos trabajan para ellos",
                "No confío en los hospitales, están todos infiltrados",
                "¿Por qué debería contarle algo? Podría ser uno de ellos",
                "¿Cómo sé que no es un agente encubierto?",
                "Sus preguntas son muy similares a las de los otros...",
                "Parece que ya sabe demasiado sobre mí",
                "No me gusta cómo me está mirando"
            ]
        }
        
        # Triggers específicos que aumentan la paranoia
        self.triggers = {
            'preguntas_personales': [
                'familia', 'trabajo', 'amigos', 'casa', 'vida', 'nombre', 'edad', 
                'dirección', 'teléfono', 'correo', 'dinero', 'banco', 'cuenta', 
                'pasado', 'futuro', 'planes', 'rutina', 'horario'
            ],
            'autoridad': [
                'doctor', 'policía', 'gobierno', 'hospital', 'ley', 'agente', 
                'seguridad', 'guardia', 'enfermero', 'enfermera', 'psiquiatra', 
                'terapeuta', 'juez', 'abogado', 'sistema'
            ],
            'vigilancia': [
                'observar', 'vigilar', 'seguir', 'notar', 'ver', 'mirar', 'espiar',
                'controlar', 'rastrear', 'monitorear', 'grabar', 'escuchar', 'investigar',
                'analizar', 'examinar', 'estudiar', 'supervisar'
            ],
            'control': [
                'ayudar', 'medicar', 'tratar', 'calmar', 'controlar', 'mejorar',
                'curar', 'sanar', 'recuperar', 'normalizar', 'ajustar', 'cambiar',
                'modificar', 'regular', 'supervisar', 'manejar', 'gestionar'
            ]
        }
        
        # Respuestas evasivas cuando se siente amenazado
        self.evasivas = [
            "*Murmurando* No es seguro hablar de eso...",
            "*Mirando hacia la puerta* ¿Escuchó eso?",
            "Prefiero no discutir eso aquí... las paredes tienen oídos",
            "*Nerviosamente* Hay cosas que es mejor no decir",
            "No puedo... no debo... es peligroso",
            "*Ajustándose el cuello de la camisa* Hace calor aquí, ¿no?",
            "*Moviendo la pierna nerviosamente* Mejor hablemos de otra cosa",
            "¿Podríamos cambiar de tema? Este me pone... nervioso",
            "*Mirando el reloj* ¿No es hora de terminar ya?",
            "*Frotándose las manos* Algunas preguntas son peligrosas...",
            "Hay cosas que es mejor mantener en secreto",
            "*Bajando la voz* No aquí... no es seguro"
        ]

    def analizar_entrada(self, entrada):
        entrada = entrada.lower()
        nivel_amenaza = 0
        
        # Detectar patrones de amenaza
        if '?' in entrada:
            nivel_amenaza += 3  # Preguntas son sospechosas
            if any(palabra in entrada for palabra in self.triggers['preguntas_personales']):
                return random.choice(self.patrones_pensamiento['interrogatorio'])
        
        # Detectar intentos de control o manipulación
        if any(palabra in entrada for palabra in self.triggers['control']):
            self.desconfianza += 5
            return random.choice(self.patrones_pensamiento['desconfianza'])
        
        # Reaccionar a menciones de autoridad
        if any(palabra in entrada for palabra in self.triggers['autoridad']):
            self.miedo += 4
            return f"*Tensándose visiblemente* {random.choice(self.patrones_pensamiento['amenaza'])}"
        
        # Reaccionar a temas de vigilancia
        if any(palabra in entrada for palabra in self.triggers['vigilancia']):
            self.miedo += 5
            return random.choice(self.creencias_core.values())
        
        return None

    def responder(self, entrada):
        time.sleep(1.5)  # Pausa más larga para simular desconfianza
        
        # Analizar si la entrada representa una amenaza
        respuesta_inmediata = self.analizar_entrada(entrada)
        if respuesta_inmediata:
            return respuesta_inmediata
        
        # Comportamiento base paranoide
        if random.random() < 0.3:  # 30% de chance de ser evasivo
            return random.choice(self.evasivas)
        
        # Respuestas basadas en nivel de amenaza percibida
        if self.desconfianza > 20:
            self.desconfianza -= 2
            return f"*Con voz temblorosa* {random.choice(self.patrones_pensamiento['amenaza'])}"
        elif self.miedo > 15:
            self.miedo -= 2
            return random.choice(list(self.creencias_core.values()))
        else:
            return random.choice(self.patrones_pensamiento['desconfianza'])

def main():
    print("\n" + "*" * 78)
    print("*  P.A.R.R.Y. Simulador de Paciente Paranoide")
    print("*  Versión en español basada en el programa original de 1972")
    print("*  por Kenneth Colby")
    print("*")
    print("*  Este programa simula a un paciente con paranoia esquizofrénica, uno de los")
    print("*  primeros programas en pasar una versión del Test de Turing. PARRY era conocido")
    print("*  por su personalidad paranoide y sus teorías conspirativas sobre la mafia.")
    print("*")
    print("*  PARRY fue creado para simular los patrones de pensamiento y comportamiento")
    print("*  de un paciente con esquizofrenia paranoide, incluyendo delirios sistemáticos,")
    print("*  susceptibilidad, y una historia coherente sobre la mafia y el hipódromo.")
    print("*" + "*" * 71)
    print("\nDOCTOR: Buenos días. ¿Qué le trae por aquí hoy?")
    print("(Para terminar la sesión, escriba 'adios' o 'salir')\n")
    
    parry = Parry()
    
    while True:
        entrada = input("\nDOCTOR: ").strip()
        
        if entrada.lower() in ['adios', 'salir', 'adiós']:
            print("\nPARRY: *Se levanta nerviosamente*")
            print("       No confío en que esta conversación sea privada...")
            print("       *Se va mirando sobre su hombro*")
            break
            
        respuesta = parry.responder(entrada)
        print("PARRY:", respuesta)

if __name__ == "__main__":
    main() 