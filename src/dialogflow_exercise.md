# Building a Spanish Restaurant Reservation Chatbot with Dialogflow

## Introduction
This guide will walk you through creating a Spanish-speaking restaurant reservation chatbot using Dialogflow. We'll create a system that can handle reservations, answer questions about the restaurant, and provide a natural conversational flow.

## Project Overview
Our chatbot will be able to:
- Take restaurant reservations
- Handle different party sizes
- Manage date and time preferences
- Answer questions about the restaurant's location and hours
- Provide menu information
- Handle confirmation and cancellation
- Support natural conversation flow

## Initial Setup

### Creating Your Agent
1. Go to console.dialogflow.com
2. Click "Create New Agent"
3. Name your agent "RestauranteBot"
4. Set the default language to "Spanish"
5. Click "Create"

### Enabling Spanish Language Support
```text
Important: While we're creating a Spanish chatbot, write your intent and entity names 
in English for better organization, but make all training phrases and responses in Spanish.
```

## Part 1: Creating Basic Intents

### 1. Welcome Intent
First, modify the Default Welcome Intent:

Training Phrases (in Spanish):
- Hola
- Buenos días
- Buenas tardes
- Quisiera hacer una reserva
- ¿Están abiertos?

Response:
- "¡Bienvenido a [Nombre del Restaurante]! ¿En qué puedo ayudarle hoy?"

#### Understanding Intent Detection Confidence

After setting up these training phrases, you can test how Dialogflow's Natural Language Understanding (NLU) works with variations. Try these example inputs in the test console:

```text
Test Phrases:
- "Hola buenos días"           (Combination of greetings)
- "Buenas, ¿qué tal?"         (Informal variation)
- "Muy buenas"                (Shortened greeting)
- "Hey, ¿están abiertos?"     (Mixed casual/formal)
```

Important Learning Point:
```text
When you test these phrases, look at the JSON response in the Dialogflow console. 
You'll find a "confidence" score that shows how sure the model is about matching 
the input to this intent. For example:

{
  "intent": {
    "name": "Default Welcome Intent",
    "displayName": "Default Welcome Intent",
    "confidence": 0.92
  }
}

- Scores above 0.8 indicate high confidence
- Scores between 0.6-0.8 suggest moderate confidence
- Scores below 0.6 might need additional training phrases
```

This understanding of confidence scores will help you:
1. Identify when you need more training phrases
2. Understand how Dialogflow handles variations
3. Improve your intent recognition accuracy

### 2. Make Reservation Intent
Create a new intent named "make_reservation":

Training Phrases:
- Quiero hacer una reserva
- Necesito una mesa
- ¿Tienen mesa disponible?
- Quisiera reservar una mesa
- ¿Puedo hacer una reservación?

Response:
- "Por supuesto"

#### Testing the Flow - Important Note for Students:
```text
At this point, test the conversation flow to see how it works:

1. User: "Quisiera hacer una reserva"
   Bot: "Por supuesto"

Notice how this shorter, more natural response works better because:
- It sounds more human-like
- It doesn't immediately jump to asking for information
- It gives a quick acknowledgment, similar to how a real host would respond

The question about the number of people will come in the next intent through 
the required parameters, creating a more natural back-and-forth conversation.

Common Testing Scenarios to Try:
- "Quiero reservar una mesa"
- "¿Puedo hacer una reservación?"
- "Necesito una mesa para esta noche"

Watch how the bot consistently responds with just "Por supuesto", making the 
conversation feel more natural before proceeding to collect details.
```

#### Next Step - Parameter Collection:
After this acknowledgment, we'll set up required parameters to collect reservation details. This separation of responses creates a more natural conversation flow.

## Part 2: Setting Up Entities

## Understanding System Entities

Important: System entities (@sys.number, @sys.date, @sys.time) become available only when you:
1. Create training phrases in your intents
2. Highlight/annotate the relevant parts
3. Map them to the corresponding system entity

Let's set this up step by step:

### 1. Number of People Entity (@sys.number)

In your `make_reservation` intent, add these training phrases and map the numbers:

```text
Training Phrases:
- "Necesito una mesa para cinco personas"
             (highlight "cinco" → @sys.number)
- "Somos 4"
        (highlight "4" → @sys.number)
- "Quiero reservar para 8 personas"
                      (highlight "8" → @sys.number)
- "Una mesa para dos"
                (highlight "dos" → @sys.number)
```

### 2. Date Entity (@sys.date)

Add these phrases and map the dates:

```text
- "Quisiera reservar para mañana"
                        (highlight "mañana" → @sys.date)
- "¿Tienen mesa para el 15 de julio?"
                        (highlight "15 de julio" → @sys.date)
- "Para este viernes"
           (highlight "este viernes" → @sys.date)
```

### 3. Time Entity (@sys.time)

Add these phrases and map the times:

```text
- "Quiero reservar para las 8 de la noche"
                           (highlight "8 de la noche" → @sys.time)
- "¿Hay mesa a las 14:30?"
                 (highlight "14:30" → @sys.time)
- "Para las nueve y media"
           (highlight "nueve y media" → @sys.time)
```

#### Steps to Map System Entities:
1. In your intent, enter a training phrase
2. Highlight the relevant text (number, date, or time)
3. In the entity dropdown that appears, select the appropriate @sys entity
4. Dialogflow will then recognize similar patterns in future user inputs

```text
Important Testing Note:
After mapping these entities, test with variations to see how Dialogflow handles them:

Numbers:
- "2 personas" vs "dos personas"
- "5" vs "cinco"

Dates:
- "mañana" vs "el 24 de febrero"
- "este sábado" vs "el fin de semana"

Times:
- "3 pm" vs "15:00"
- "ocho de la noche" vs "20:00"
```

Remember: The system entities only become functional after you've properly mapped them in your training phrases. The more variations you include in your training phrases, the better Dialogflow will understand different ways users might express numbers, dates, and times.

### 4. Custom Entity: Table Location
Create a new entity named "table_location":

Values:
- interior
  - Synonyms: adentro, dentro, sala principal
- terraza
  - Synonyms: afuera, exterior, al aire libre
- barra
  - Synonyms: bar, área del bar

## Part 3: Creating the Reservation Flow

### Step 1: Initial Reservation Intent
Intent Name: `make_reservation`

Required Parameters:
1. people (number)
2. date
3. time
4. location (optional)

Parameter Prompts:
Add multiple response variations for each parameter to make conversations feel more natural and less robotic.

people:
```text
Response Variations:
1. "¿Para cuántas personas necesita la reserva?"
2. "¿Cuántos comensales serán?"
3. "¿Cuántas personas van a venir?"
```

date:
```text
Response Variations:
1. "¿Qué día le gustaría venir?"
2. "¿Para qué fecha desea hacer la reserva?"
3. "¿Cuándo le gustaría visitarnos?"
```

time:
```text
Response Variations:
1. "¿A qué hora prefiere su reserva?"
2. "¿A qué hora le gustaría venir?"
3. "¿Qué horario le vendría mejor?"
```

location:
```text
Response Variations:
1. "¿Prefiere sentarse en el interior, en la terraza o en la barra?"
2. "¿Dónde le gustaría sentarse: interior, terraza o barra?"
3. "¿Tiene alguna preferencia de ubicación? Tenemos interior, terraza y barra disponibles."
```

#### Testing Prompt Variations:
```text
Important Learning Point:
1. Run through the reservation flow multiple times
2. Notice how Dialogflow randomly selects from your response variations
3. This creates a more dynamic, natural-feeling conversation
4. Users won't feel like they're talking to a script

Test the complete flow several times to see how different combinations 
of these responses work together. Pay attention to how the varying 
language makes the conversation feel more human-like.
```

Pro Tips:
- Keep a consistent level of formality across all variations
- Ensure all variations clearly ask for the same information
- Consider adding more variations as you see how users interact with your bot
- Test the variations with different user inputs to ensure they all make sense in context

### Step 2: Follow-up Intents

#### Why Do We Need Follow-up Intents?
```text
Important Concept:
Follow-up intents are crucial because they maintain the context of the conversation. 
Think about this real conversation:

Host: "¿Entonces sería una mesa para 4 personas este viernes a las 8?"
Customer: "Sí"

The "Sí" only makes sense because it's following the previous question. Without 
context, "Sí" could mean anything!
```

#### Understanding the Difference
```text
Compare these two approaches:

1. WITHOUT Follow-up Intents:
   User: "Quiero reservar una mesa"
   Bot: "¿Para cuántas personas?"
   User: "Sí"
   Bot: [Confused because "Sí" matches multiple intents]

2. WITH Follow-up Intents:
   User: "Quiero reservar una mesa"
   Bot: "¿Para cuántas personas?"
   User: "Sí"
   Bot: [Knows this "Sí" is related to the reservation confirmation 
        because it's a follow-up intent]
```

#### Benefits of Follow-up Intents:
1. **Context Awareness**: Follow-ups understand the conversation flow
2. **Reduced Confusion**: Prevents mixing up similar responses in different contexts
3. **Better Organization**: Keeps related intents grouped together
4. **Improved Accuracy**: Higher confidence in intent matching due to context

#### Testing Tip:
```text
Try this experiment in your bot:

1. Create a regular intent for "Sí"
2. Create a follow-up intent for "Sí"
3. Test both in different contexts
4. Notice how the follow-up intent only triggers when it should

This will help you understand why follow-ups are essential for natural 
conversation flows.
```

Create these follow-up intents under `make_reservation`:

1. make_reservation.confirm
   - Training Phrases:
     - Sí, está bien
     - Me parece bien
     - Confirmo
     - Perfecto
   
2. make_reservation.cancel
   - Training Phrases:
     - No, gracias
     - Mejor no
     - Cancelar
     - No quiero hacer la reserva

## Part 4: Setting Up Context

Think of context like a waiter's memory during service. When you're at a restaurant and say "I'll take that too", the waiter knows what "that" means because they remember what was just discussed. In Dialogflow, context works the same way - it's how your chatbot remembers the current conversation state.

```text
For example:
User: "Quiero hacer una reserva"
Bot: "Por supuesto. ¿Para cuántas personas?"
User: "Para 4"
Bot: "¿Qué día le gustaría venir?"
User: "Mejor no"              <- Without context, "Mejor no" could mean anything
                                With context, the bot knows you're canceling
                                the reservation process
```

Context helps your chatbot:
- Remember what's being discussed
- Understand what stage of the conversation you're in
- Know when a user can say certain things
- Clear its "memory" when a conversation topic ends

The context's lifespan (measured in turns of conversation) determines how long the bot should remember this information. Think carefully about these lifespans - too short and the bot forgets too quickly, too long and it might remember things it should have forgotten.

### Context Configuration

1. In the `make_reservation` intent:
   - Output Context: `awaiting_reservation_confirmation`
   - Lifespan: 5

2. In make_reservation.confirm:
   - Input Context: `awaiting_reservation_confirmation`
   - Output Context: `reservation_confirmed`
   - Lifespan: 5

3. In make_reservation.cancel:
   - Input Context: `awaiting_reservation_confirmation`
   - Output Context: `reservation_cancelled`
   - Lifespan: 2

### Response Management

For `make_reservation`, after collecting all parameters:
```text
"Perfecto. Entonces sería una reserva para $people personas, el día $date a las $time${location ? ' en ' + location : ''}. ¿Desea confirmar esta reserva?"
```

For `make_reservation.confirm`:
```text
"¡Excelente! Su reserva está confirmada. Le esperamos el $date a las $time. ¿Necesita algo más?"
```

For `make_reservation.cancel`:
```text
"Entiendo. No hay problema. ¿Hay algo más en lo que pueda ayudarle?"
```

## Part 5: Additional Features

### Restaurant Information Intent
Create an intent named `restaurant_info`:

Training Phrases:
- ¿Dónde están ubicados?
- ¿Cuál es su dirección?
- ¿Cómo llego al restaurante?
- ¿Cuál es su horario?
- ¿Hasta qué hora están abiertos?

Response:
```text
"Estamos ubicados en [dirección]. Nuestro horario es de [horario]. Puede encontrar indicaciones en nuestro sitio web [sitio web]."
```

### Menu Information Intent
Create an intent named `menu_info`:

Training Phrases:
- ¿Qué tipo de comida tienen?
- ¿Puedo ver el menú?
- ¿Tienen platos vegetarianos?
- ¿Cuál es el especial del día?

Response:
```text
"Ofrecemos una variada selección de platos tradicionales y modernos. Puede consultar nuestro menú completo en [enlace al menú]. ¿Le gustaría que le recomiende algún plato en particular?"
```

## Testing Your Chatbot

### Test Scenarios
Run through these conversations to ensure proper functionality:

1. Basic Reservation:
```text
Usuario: Hola
Bot: ¡Bienvenido a [Restaurante]! ¿En qué puedo ayudarle hoy?
Usuario: Quiero hacer una reserva
Bot: Por supuesto. ¿Para cuántas personas necesita la reserva?
Usuario: 4 personas
Bot: ¿Qué día le gustaría venir?
[Continue conversation...]
```

2. Complex Scenario:
```text
Usuario: Quisiera reservar una mesa para mañana
Bot: ¿Para cuántas personas necesita la reserva?
Usuario: Seremos 6, en la terraza si es posible
Bot: ¿A qué hora prefiere su reserva?
[Continue conversation...]
```

## Troubleshooting Tips

Common Issues and Solutions:
1. Entity Recognition Problems
   - Double-check entity annotations in training phrases
   - Add more training phrases with variations
   - Verify system entities are properly configured

2. Context Issues
   - Verify context lifespans
   - Check input/output context connections
   - Test conversation flows thoroughly

3. Language Understanding
   - Add regional variations of Spanish phrases
   - Include common spelling mistakes
   - Consider different ways to express the same intent

## Best Practices

1. Training Phrases
   - Include at least 15-20 training phrases per intent
   - Use variations in word order
   - Include common mistakes and informal language

2. Responses
   - Keep them natural and conversational
   - Include variation in responses
   - Use appropriate formality level

3. Context Management
   - Keep context lifespans reasonable
   - Clear contexts when conversations end
   - Use meaningful context names

## Maintenance and Improvement

Regular Updates:
1. Review conversation logs weekly
2. Add new training phrases based on user interactions
3. Adjust responses based on user feedback
4. Monitor performance metrics
5. Update menu items and restaurant information as needed

Remember to regularly test the chatbot with different scenarios and keep improving its understanding based on actual user interactions.