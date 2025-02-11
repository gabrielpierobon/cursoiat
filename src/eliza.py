import re
import random
import time

class Eliza:
    def __init__(self):
        self.patrones = [
            (r'.*\b(triste|deprimido|deprimida|mal|solo|sola|infeliz|angustiado|angustiada)\b.*', [
                "¿Por qué te sientes {}?",
                "Cuéntame más sobre esos sentimientos.",
                "¿Desde cuándo te sientes {}?",
                "¿Hay algo específico que te haga sentir {}?",
                "¿Qué crees que podría ayudarte a no sentirte {}?"
            ]),
            (r'.*\b(feliz|contento|contenta|bien|mejor|alegre|genial|estupendo|estupenda)\b.*', [
                "¿Qué te hace sentir {}?",
                "Me alegra que te sientas {}.",
                "¿Por qué crees que te sientes {}?",
                "¿Qué ha cambiado para que te sientas {}?",
                "Cuéntame más sobre las cosas que te hacen sentir {}"
            ]),
            (r'.*\b(madre|padre|papá|mamá|hermano|hermana|familia)\b.*', [
                "Háblame más sobre tu familia.",
                "¿Qué relación tienes con tu familia?",
                "¿Cómo te hace sentir tu familia?",
                "¿Desde cuándo te sientes así respecto a tu familia?",
                "¿Cómo crees que tu familia ve la situación?"
            ]),
            (r'.*\b(siempre|nunca|todos|nadie|todo|nada)\b.*', [
                "¿Estás seguro que {}?",
                "¿Por qué piensas que {}?",
                "¿'{}' no es una palabra muy absoluta?",
                "¿Ha habido excepciones a ese '{}'?",
                "¿Qué pasaría si hubiera excepciones?"
            ]),
            (r'.*\b(quiero|deseo|necesito|anhelo)\b.*', [
                "¿Por qué {} eso?",
                "¿Qué harías si lo consiguieras?",
                "¿Qué te impide conseguirlo?",
                "¿Desde cuándo {} eso?",
                "¿Qué sería diferente en tu vida si lo consiguieras?"
            ]),
            (r'.*\b(no puedo|imposible|difícil|complicado)\b.*', [
                "¿Por qué crees que no puedes?",
                "¿Qué pasaría si pudieras?",
                "¿Qué te lo impide?",
                "¿Siempre ha sido así?",
                "¿Qué necesitarías para poder hacerlo?"
            ]),
            (r'.*\b(preocupa|problema|miedo|asusta|inquieta)\b.*', [
                "¿Qué es lo que más te preocupa de eso?",
                "¿Has hablado con alguien más sobre esta preocupación?",
                "¿Cómo manejas esa preocupación?",
                "¿Desde cuándo te preocupa esto?",
                "¿Qué sería lo peor que podría pasar?"
            ]),
            (r'.*\b(amigo|amiga|novio|novia|pareja|relación)\b.*', [
                "¿Cómo te sientes en esa relación?",
                "¿Qué esperas de esa relación?",
                "¿Has hablado de esto con esa persona?",
                "¿Cómo crees que la otra persona se siente?",
                "¿Qué te gustaría que fuera diferente en esa relación?"
            ]),
            (r'.*\b(trabajo|estudio|carrera|universidad|escuela)\b.*', [
                "¿Cómo te sientes con eso?",
                "¿Qué te gustaría cambiar?",
                "¿Qué te motiva a seguir?",
                "¿Cuáles son tus objetivos?",
                "¿Qué te impide alcanzar tus metas?"
            ]),
            (r'.*\b(antes|pasado|recuerdo|extraño|añoro)\b.*', [
                "¿Cómo te hace sentir recordar eso?",
                "¿Qué has aprendido de esa experiencia?",
                "¿Cómo ha influido eso en quien eres ahora?",
                "¿Qué te gustaría haber hecho diferente?",
                "¿Qué consejo le darías a tu yo del pasado?"
            ])
        ]
        
        self.respuestas_genericas = [
            "Cuéntame más sobre eso.",
            "¿Cómo te hace sentir eso?",
            "¿Por qué piensas eso?",
            "Continúa...",
            "¿Podrías elaborar más?",
            "Entiendo... ¿y qué más?",
            "¿Qué piensas tú sobre eso?",
            "¿Qué te hace pensar eso?",
            "¿Cómo llegaste a esa conclusión?",
            "¿Qué significa eso para ti?",
            "Interesante... ¿podrías profundizar en eso?",
            "¿Cómo te afecta eso en tu día a día?",
            "¿Qué sentimientos te genera eso?",
            "¿Hay algo más que quieras compartir al respecto?"
        ]

    def responder(self, entrada):
        time.sleep(2)
        if not entrada.strip():
            return "Por favor, dime algo."
            
        # Convertir la entrada a minúsculas para facilitar el matching
        entrada = entrada.lower()
        
        for patron, respuestas in self.patrones:
            match = re.match(patron, entrada)
            if match:
                # Si el patrón tiene grupos, usar el primer grupo encontrado
                if len(match.groups()) > 0:
                    return random.choice(respuestas).format(match.group(1))
                return random.choice(respuestas)
        
        return random.choice(self.respuestas_genericas)

def main():
    print("\n" + "*" * 78)
    print("*  E.L.I.Z.A. Simulador de Psicoterapeuta")
    print("*  Versión en español basada en el programa original de 1966")
    print("*  por Joseph Weizenbaum")
    print("*")
    print("*  Este programa simula un psicoterapeuta rogeriano que utiliza terapia centrada")
    print("*  en la persona. La terapia rogeriana, desarrollada por Carl Rogers, se basa en la")
    print("*  escucha activa y la empatía. El terapeuta refleja y reformula lo que dice el")
    print("*  paciente, ayudándole a explorar sus propios pensamientos y sentimientos sin")
    print("*  juzgar ni dirigir.")
    print("*" + "*" * 71)
    print("\nELIZA: Hola, soy tu psicoterapeuta. ¿En qué puedo ayudarte hoy?")
    print("(Para terminar la conversación, escribe 'adios' o 'salir')\n")
    
    while True:
        entrada = input("\nTú: ").strip()
        
        if entrada.lower() in ['adios', 'salir', 'adiós']:
            print("\nELIZA: Ha sido un placer hablar contigo. Espero que te sientas mejor.")
            print("       ¡Hasta pronto!")
            break
            
        respuesta = eliza.responder(entrada)
        print("ELIZA:", respuesta)

if __name__ == "__main__":
    eliza = Eliza()
    main() 