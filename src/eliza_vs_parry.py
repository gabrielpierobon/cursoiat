from eliza import Eliza
from parry import Parry
import time
import random
import re

class Debate:
    def __init__(self):
        self.eliza = Eliza()
        self.parry = Parry()
        
        # Frases iniciales de ELIZA
        self.inicios_eliza = [
            "Buenas tardes. Cuénteme sus problemas",
            "¿Cómo se siente hoy?",
            "¿Qué le trae por aquí?",
            "¿De qué le gustaría hablar?"
        ]
        
        # Patrones de espejo específicos para este debate
        self.patrones_espejo = [
            # Patrones basados en el diálogo original
            (r'.*la gente (.+)', "¿Por qué dice que la gente {}?"),
            (r'.*(?:usted|tu) debería (.+)', "Suponga que debería {}"),
            (r'.*no (?:entiendo|comprendo) (.+)', "¿Qué es lo que no entiende de {}?"),
            (r'.*me molesta estar (.+)', "¿Qué le sugiere el estar {}?"),
            (r'.*fui al (.+)', "¿Qué significa para usted haber ido al {}?"),
            
            # Patrones adicionales para más variedad
            (r'.*(?:me siguen|me persiguen) (.+)', "¿Desde cuándo siente que lo {}?"),
            (r'.*(?:no puedo|no quiero) (.+)', "¿Qué pasaría si pudiera {}?"),
            (r'.*tengo miedo de (.+)', "¿Qué le hace temer {}?"),
            (r'.*(?:creo|pienso) que (.+)', "¿Por qué cree que {}?"),
            (r'.*estoy cansado de (.+)', "Cuénteme más sobre por qué está cansado de {}")
        ]
        
        # Respuestas de seguimiento para profundizar
        self.seguimientos = [
            "¿Podría elaborar más sobre eso?",
            "¿Desde cuándo se siente así?",
            "Continúe, lo escucho",
            "¿Qué más puede decirme al respecto?",
            "Entiendo. ¿Y qué más?",
            "¿Cómo le hace sentir eso?"
        ]
        
        self.turnos = 0
        self.max_turnos = 15
        self.ultima_respuesta = ""  # Para evitar repeticiones

    def formatear_mensaje(self, quien, mensaje):
        print(f"\n{quien}: {mensaje}")
        # Pausa aleatoria continua entre 2.0 y 5.0 segundos
        pausa = random.uniform(2.0, 5.0)
        time.sleep(pausa)

    def respuesta_espejo(self, mensaje):
        # 50% de probabilidad de usar respuesta espejo
        if random.random() < 0.5:
            for patron, respuesta in self.patrones_espejo:
                match = re.match(patron, mensaje.lower())
                if match:
                    return respuesta.format(match.group(1))
        return None

    def obtener_respuesta_eliza(self, mensaje_parry):
        # Evitar repeticiones y alternar entre tipos de respuestas
        respuesta_espejo = self.respuesta_espejo(mensaje_parry)
        
        if respuesta_espejo and respuesta_espejo != self.ultima_respuesta:
            self.ultima_respuesta = respuesta_espejo
            return respuesta_espejo
        
        # Si no hay espejo o sería repetición, usar respuesta normal de ELIZA
        respuesta_normal = self.eliza.responder(mensaje_parry)
        
        # Si la respuesta normal es muy genérica, intentar un seguimiento
        if respuesta_normal in ["Continúe...", "Cuénteme más sobre eso."]:
            respuesta_normal = random.choice(self.seguimientos)
        
        self.ultima_respuesta = respuesta_normal
        return respuesta_normal

    def debatir(self):
        print("\n" + "*" * 78)
        print("*  ELIZA vs PARRY - Debate Histórico")
        print("*  Una recreación del primer debate entre chatbots de la historia")
        print("*  ELIZA (1966) vs PARRY (1972)")
        print("*")
        print("*  ELIZA: Psicoterapeuta rogeriana")
        print("*  PARRY: Paciente con paranoia esquizofrénica")
        print("*" + "*" * 71)
        
        mensaje_actual = self.inicios_eliza[0]
        self.formatear_mensaje("ELIZA", mensaje_actual)
        
        while self.turnos < self.max_turnos:
            # PARRY responde a ELIZA
            respuesta_parry = self.parry.responder(mensaje_actual)
            self.formatear_mensaje("PARRY", respuesta_parry)
            self.turnos += 1
            
            if self.turnos >= self.max_turnos:
                break
            
            # ELIZA responde a PARRY
            respuesta_eliza = self.obtener_respuesta_eliza(respuesta_parry)
            self.formatear_mensaje("ELIZA", respuesta_eliza)
            mensaje_actual = respuesta_eliza
            self.turnos += 1
        
        print("\n" + "*" * 78)
        print(f"*  Fin del debate - {self.max_turnos} intercambios completados")
        print("*" + "*" * 71)

def main():
    debate = Debate()
    debate.debatir()

if __name__ == "__main__":
    main() 