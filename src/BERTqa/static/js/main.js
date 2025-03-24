// Declaración de variables globales
let isProcessing = false;
let currentContext = '';
let questionHistory = [];

// Referencias a los elementos DOM
const contextInput = document.getElementById('context-input');
const questionForm = document.getElementById('question-form');
const questionInput = document.getElementById('question-input');
const submitBtn = document.getElementById('submit-btn');
const clearContextBtn = document.getElementById('clear-context');
const qaHistoryContainer = document.getElementById('qa-history');
const newConversationBtn = document.getElementById('new-conversation-btn');
const examplesList = document.getElementById('examples-list');
const modelStatus = document.getElementById('model-status');

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    // Cargar la información del modelo
    fetchModelInfo();
    
    // Cargar ejemplos
    fetchExamples();
    
    // Añadir un mensaje de bienvenida del sistema
    addSystemMessage('¡Bienvenido a BERT-QA! Proporciona un contexto en el área superior y haz preguntas sobre ese contexto. El modelo BERT analizará el texto y responderá basándose únicamente en la información proporcionada.');
    
    // Configurar event listeners
    setupEventListeners();
});

// Configurar los event listeners
function setupEventListeners() {
    // Formulario de preguntas
    questionForm.addEventListener('submit', handleQuestionSubmit);
    
    // Validación de entrada
    questionInput.addEventListener('input', validateInputs);
    contextInput.addEventListener('input', validateInputs);
    
    // Botón para limpiar contexto
    clearContextBtn.addEventListener('click', clearContext);
    
    // Botón para nueva conversación
    newConversationBtn.addEventListener('click', startNewConversation);
}

// Validar entradas y habilitar/deshabilitar botón de envío
function validateInputs() {
    const hasContext = contextInput.value.trim().length > 10;
    const hasQuestion = questionInput.value.trim().length > 0;
    
    submitBtn.disabled = !hasContext || !hasQuestion || isProcessing;
    
    // Guardar el contexto actual
    currentContext = contextInput.value.trim();
}

// Manejar el envío de una pregunta
async function handleQuestionSubmit(e) {
    e.preventDefault();
    
    if (isProcessing) return;
    
    const context = contextInput.value.trim();
    const question = questionInput.value.trim();
    
    if (!context || !question) return;
    
    // Actualizar estado
    isProcessing = true;
    submitBtn.disabled = true;
    
    // Añadir la pregunta a la interfaz
    addQuestionToUI(question);
    
    // Mostrar estado de carga
    const loadingElement = addLoadingState();
    
    try {
        // Enviar la pregunta a la API
        console.log('Enviando pregunta a la API:', { context, question });
        const response = await fetch('/api/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                context,
                question
            })
        });
        
        // Comprobar si la respuesta es correcta
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error en respuesta de API:', response.status, errorText);
            throw new Error(`Error al procesar la pregunta (${response.status}): ${errorText}`);
        }
        
        // Obtener la respuesta
        const data = await response.json();
        console.log('Respuesta recibida de la API:', data);
        
        // Eliminar el estado de carga
        loadingElement.remove();
        
        // Si hay error en la respuesta, mostrar el error
        if (!data.success || data.error) {
            throw new Error(data.error || 'Error en la respuesta del servidor');
        }
        
        // Añadir la respuesta a la interfaz
        addAnswerToUI(data);
        
        // Añadir a la historia
        questionHistory.push({ question, answer: data.answer, highlight: data.highlight });
        
    } catch (error) {
        console.error('Error:', error);
        
        // Eliminar el estado de carga
        loadingElement.remove();
        
        // Mostrar error en la interfaz
        addErrorToUI(error.message || 'Ocurrió un error al procesar tu pregunta');
    } finally {
        // Restaurar estado
        isProcessing = false;
        submitBtn.disabled = false;
        
        // Limpiar el campo de pregunta
        questionInput.value = '';
        questionInput.focus();
        
        // Actualizar validación
        validateInputs();
    }
}

// Añadir pregunta a la interfaz
function addQuestionToUI(question) {
    const questionTemplate = document.getElementById('question-template').content.cloneNode(true);
    questionTemplate.querySelector('.question-text').textContent = question;
    
    qaHistoryContainer.appendChild(questionTemplate);
    
    // Hacer scroll hasta la nueva pregunta
    qaHistoryContainer.scrollTop = qaHistoryContainer.scrollHeight;
}

// Añadir estado de carga
function addLoadingState() {
    const loadingTemplate = document.getElementById('loading-template').content.cloneNode(true);
    qaHistoryContainer.appendChild(loadingTemplate);
    
    // Hacer scroll hasta el indicador de carga
    qaHistoryContainer.scrollTop = qaHistoryContainer.scrollHeight;
    
    // Devolver el elemento para poder eliminarlo más tarde
    return qaHistoryContainer.lastElementChild;
}

// Añadir respuesta a la interfaz
function addAnswerToUI(data) {
    const answerTemplate = document.getElementById('answer-template').content.cloneNode(true);
    
    // Establecer el texto de la respuesta
    answerTemplate.querySelector('.answer-text').textContent = data.answer;
    
    // Añadir el texto resaltado si existe
    if (data.highlight && data.highlight.trim().length > 0) {
        const highlightElement = answerTemplate.querySelector('.answer-highlight');
        highlightElement.innerHTML = `<strong>Pasaje relevante:</strong> ${data.highlight}`;
        highlightElement.style.display = 'block';
    } else {
        answerTemplate.querySelector('.answer-highlight').style.display = 'none';
    }
    
    // Añadir metadatos
    if (data.score) {
        answerTemplate.querySelector('.answer-confidence').textContent = `Confianza: ${(data.score * 100).toFixed(1)}%`;
    }
    
    if (data.time) {
        answerTemplate.querySelector('.answer-time').textContent = `Tiempo: ${data.time.toFixed(2)}s`;
    }
    
    // Añadir al último elemento qa-pair en lugar de crear uno nuevo
    const lastQAPair = qaHistoryContainer.querySelector('.qa-pair:last-child');
    if (lastQAPair) {
        lastQAPair.appendChild(answerTemplate);
    } else {
        // Si por alguna razón no hay un qa-pair, crear uno completo
        const questionTemplate = document.getElementById('question-template').content.cloneNode(true);
        questionTemplate.querySelector('.question-text').textContent = "Pregunta anterior";
        const qaElement = document.importNode(questionTemplate, true);
        qaElement.appendChild(answerTemplate);
        qaHistoryContainer.appendChild(qaElement);
    }
    
    // Hacer scroll hasta la nueva respuesta
    qaHistoryContainer.scrollTop = qaHistoryContainer.scrollHeight;
}

// Añadir mensaje de error a la interfaz
function addErrorToUI(errorMsg) {
    const errorTemplate = document.getElementById('error-template').content.cloneNode(true);
    errorTemplate.querySelector('.error-text').textContent = errorMsg;
    
    qaHistoryContainer.appendChild(errorTemplate);
    
    // Hacer scroll hasta el error
    qaHistoryContainer.scrollTop = qaHistoryContainer.scrollHeight;
}

// Añadir mensaje del sistema a la interfaz
function addSystemMessage(message) {
    const systemTemplate = document.getElementById('system-message-template').content.cloneNode(true);
    systemTemplate.querySelector('.system-message').textContent = message;
    
    qaHistoryContainer.appendChild(systemTemplate);
}

// Limpiar el contexto
function clearContext() {
    contextInput.value = '';
    validateInputs();
    contextInput.focus();
}

// Iniciar una nueva conversación
function startNewConversation() {
    // Limpiar el contexto y la pregunta
    clearContext();
    questionInput.value = '';
    
    // Limpiar el historial de preguntas/respuestas
    qaHistoryContainer.innerHTML = '';
    questionHistory = [];
    
    // Añadir un mensaje de bienvenida
    addSystemMessage('¡Nueva conversación iniciada! Proporciona un contexto en el área superior y haz preguntas sobre ese contexto.');
    
    // Enfocar el campo de contexto
    contextInput.focus();
}

// Cargar ejemplos desde la API
async function fetchExamples() {
    try {
        const response = await fetch('/api/examples');
        if (!response.ok) {
            throw new Error('Error al cargar ejemplos');
        }
        
        const data = await response.json();
        
        // Limpiar contenedor de ejemplos
        examplesList.innerHTML = '';
        
        // Comprobar el formato de los datos y adaptarlos si es necesario
        let examplesArray = data;
        // Si los ejemplos están dentro de una propiedad del objeto
        if (!Array.isArray(data) && data.examples) {
            examplesArray = data.examples;
        }
        
        // Añadir ejemplos a la interfaz
        if (Array.isArray(examplesArray)) {
            examplesArray.forEach(example => {
                addExampleToUI(example);
            });
        } else {
            console.error('Los ejemplos recibidos no son un array válido:', data);
        }
    } catch (error) {
        console.error('Error cargando ejemplos:', error);
    }
}

// Añadir un ejemplo a la interfaz
function addExampleToUI(example) {
    const exampleTemplate = document.getElementById('example-template').content.cloneNode(true);
    
    // Configurar el título y la descripción
    exampleTemplate.querySelector('.example-title').textContent = example.title;
    
    // Obtener el contenedor de preguntas del ejemplo
    const questionsContainer = exampleTemplate.querySelector('.example-questions');
    
    // Añadir cada pregunta como un elemento
    example.questions.forEach(q => {
        const questionElement = document.createElement('div');
        questionElement.className = 'example-question';
        questionElement.textContent = q;
        
        // Añadir event listener para cargar el ejemplo
        questionElement.addEventListener('click', () => {
            loadExample(example.context, q);
        });
        
        questionsContainer.appendChild(questionElement);
    });
    
    // Añadir el ejemplo al contenedor
    examplesList.appendChild(exampleTemplate);
}

// Cargar un ejemplo en la interfaz
function loadExample(exampleContext, exampleQuestion) {
    // Establecer el contexto y la pregunta
    contextInput.value = exampleContext;
    questionInput.value = exampleQuestion;
    
    // Validar entradas
    validateInputs();
    
    // Hacer scroll hasta el formulario de pregunta
    questionInput.scrollIntoView({ behavior: 'smooth' });
    questionInput.focus();
}

// Obtener información del modelo
async function fetchModelInfo() {
    try {
        const response = await fetch('/api/model_info');
        if (!response.ok) {
            throw new Error('Error al cargar información del modelo');
        }
        
        const modelInfo = await response.json();
        
        // Actualizar la información del modelo en la interfaz
        updateModelInfo(modelInfo);
    } catch (error) {
        console.error('Error cargando información del modelo:', error);
        modelStatus.textContent = 'Estado: Error al cargar información';
    }
}

// Actualizar la información del modelo en la interfaz
function updateModelInfo(modelInfo) {
    const statusText = `Modelo: ${modelInfo.model_name}\nEstado: ${modelInfo.status}\nVersión: ${modelInfo.version || 'N/A'}`;
    modelStatus.textContent = statusText;
} 