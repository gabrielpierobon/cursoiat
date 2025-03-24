// Variables globales
const API_URL = '/api';
let conversation = [];
let isGenerating = false;

// Referencias a elementos del DOM
const conversationContainer = document.getElementById('conversation');
const promptForm = document.getElementById('prompt-form');
const promptInput = document.getElementById('prompt-input');
const submitBtn = document.getElementById('submit-btn');
const modelStatus = document.getElementById('model-status');
const historyList = document.getElementById('history-list');
const newChatBtn = document.getElementById('new-chat-btn');
const temperatureSlider = document.getElementById('temperature');
const temperatureValue = document.getElementById('temp-value');
const tokensSlider = document.getElementById('tokens');
const tokensValue = document.getElementById('tokens-value');
const promptButtons = document.querySelectorAll('.prompt-btn');

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    // Cargar información del modelo
    fetchModelInfo();
    
    // Configurar eventos
    setupEventListeners();
    
    // Cargar conversación guardada si existe
    loadConversation();
});

// Configurar los eventos de la interfaz
function setupEventListeners() {
    // Envío del formulario
    promptForm.addEventListener('submit', handleSubmit);
    
    // Nueva conversación
    newChatBtn.addEventListener('click', () => {
        if (confirm('¿Estás seguro de que deseas iniciar una nueva conversación? La actual se perderá.')) {
            clearConversation();
        }
    });
    
    // Sliders para temperatura y tokens
    temperatureSlider.addEventListener('input', (e) => {
        temperatureValue.textContent = e.target.value;
    });
    
    tokensSlider.addEventListener('input', (e) => {
        tokensValue.textContent = e.target.value;
    });
    
    // Botones de prompt
    promptButtons.forEach(button => {
        button.addEventListener('click', () => {
            promptInput.value = button.textContent;
            promptInput.focus();
        });
    });
}

// Manejar el envío del formulario
async function handleSubmit(e) {
    e.preventDefault();
    
    const prompt = promptInput.value.trim();
    if (!prompt || isGenerating) return;
    
    // Obtener parámetros de generación
    const temperature = parseFloat(temperatureSlider.value);
    const numTokens = parseInt(tokensSlider.value);
    
    // Agregar mensaje del usuario a la conversación
    addMessageToConversation('Tú', prompt, 'human-message');
    
    // Limpiar input y mostrar estado de carga
    promptInput.value = '';
    isGenerating = true;
    submitBtn.disabled = true;
    
    // Agregar mensaje de carga para el AI
    const loadingMessage = addLoadingMessage();
    
    // Hacer solicitud a la API
    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt,
                temperature,
                num_tokens: numTokens
            })
        });
        
        // Verificar respuesta
        if (!response.ok) {
            throw new Error(`Error al generar texto: ${response.status}`);
        }
        
        // Procesar respuesta
        const data = await response.json();
        
        // Eliminar mensaje de carga
        conversationContainer.removeChild(loadingMessage);
        
        // Agregar mensaje del AI a la conversación
        addMessageToConversation('HarryGPT', data.generated_text, 'ai-message');
        
        // Guardar la conversación
        saveConversation();
        
    } catch (error) {
        console.error('Error:', error);
        
        // Eliminar mensaje de carga
        conversationContainer.removeChild(loadingMessage);
        
        // Mostrar mensaje de error
        addMessageToConversation('Sistema', `Error: ${error.message}`, 'system-message error');
    } finally {
        // Restablecer estado
        isGenerating = false;
        submitBtn.disabled = false;
        promptInput.focus();
    }
}

// Agregar un mensaje a la conversación
function addMessageToConversation(sender, content, messageClass) {
    // Crear elementos del mensaje
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${messageClass}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Crear encabezado del mensaje con avatar
    const messageHeader = document.createElement('div');
    messageHeader.className = 'message-header';
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${messageClass === 'human-message' ? 'human-avatar' : 'ai-avatar'}`;
    
    // Icono para el avatar
    const avatarIcon = document.createElement('i');
    avatarIcon.className = messageClass === 'human-message' ? 'fas fa-user' : 'fas fa-robot';
    avatar.appendChild(avatarIcon);
    
    const senderSpan = document.createElement('span');
    senderSpan.className = 'message-sender';
    senderSpan.textContent = sender;
    
    messageHeader.appendChild(avatar);
    messageHeader.appendChild(senderSpan);
    
    // Crear contenido del mensaje
    const contentP = document.createElement('p');
    contentP.textContent = content;
    
    // Ensamblar el mensaje
    messageContent.appendChild(messageHeader);
    messageContent.appendChild(contentP);
    messageDiv.appendChild(messageContent);
    
    // Añadir a la conversación
    conversationContainer.appendChild(messageDiv);
    
    // Guardar en el array de conversación
    conversation.push({
        sender,
        content,
        messageClass
    });
    
    // Scroll al final de la conversación
    conversationContainer.scrollTop = conversationContainer.scrollHeight;
    
    return messageDiv;
}

// Agregar mensaje de carga
function addLoadingMessage() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai-message';
    
    const loadingContent = document.createElement('div');
    loadingContent.className = 'message-content';
    
    const loadingHeader = document.createElement('div');
    loadingHeader.className = 'message-header';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar ai-avatar';
    
    const avatarIcon = document.createElement('i');
    avatarIcon.className = 'fas fa-robot';
    avatar.appendChild(avatarIcon);
    
    const senderSpan = document.createElement('span');
    senderSpan.className = 'message-sender';
    senderSpan.textContent = 'HarryGPT';
    
    loadingHeader.appendChild(avatar);
    loadingHeader.appendChild(senderSpan);
    
    const loadingDots = document.createElement('div');
    loadingDots.className = 'loading-dots';
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        loadingDots.appendChild(dot);
    }
    
    loadingContent.appendChild(loadingHeader);
    loadingContent.appendChild(loadingDots);
    loadingDiv.appendChild(loadingContent);
    
    conversationContainer.appendChild(loadingDiv);
    conversationContainer.scrollTop = conversationContainer.scrollHeight;
    
    return loadingDiv;
}

// Guardar conversación en localStorage
function saveConversation() {
    if (conversation.length > 0) {
        localStorage.setItem('harryGPT_conversation', JSON.stringify(conversation));
        updateHistoryList();
    }
}

// Cargar conversación desde localStorage
function loadConversation() {
    const savedConversation = localStorage.getItem('harryGPT_conversation');
    if (savedConversation) {
        try {
            const parsedConversation = JSON.parse(savedConversation);
            
            // Limpiar conversación actual
            conversationContainer.innerHTML = '';
            
            // Mostrar los mensajes guardados
            parsedConversation.forEach(msg => {
                addMessageToConversation(msg.sender, msg.content, msg.messageClass);
            });
            
            // Actualizar array de conversación
            conversation = parsedConversation;
            
            // Actualizar historial
            updateHistoryList();
            
        } catch (error) {
            console.error('Error al cargar la conversación:', error);
        }
    }
}

// Limpiar conversación actual
function clearConversation() {
    conversationContainer.innerHTML = '';
    conversation = [];
    localStorage.removeItem('harryGPT_conversation');
    
    // Mostrar mensaje inicial
    const systemMessage = document.createElement('div');
    systemMessage.className = 'message system-message';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const welcomeP = document.createElement('p');
    welcomeP.textContent = 'Bienvenido a HarryGPT, un modelo LSTM entrenado con textos de Harry Potter. ¿Sobre qué quieres que escriba?';
    
    const suggestionP = document.createElement('p');
    suggestionP.textContent = 'Prueba con alguno de estos prompts:';
    
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'prompt-suggestions';
    
    const suggestions = [
        'Harry Potter y la piedra',
        'Hermione descubrió en la biblioteca',
        'El bosque prohibido escondía',
        'Dumbledore miró a Harry y dijo'
    ];
    
    suggestions.forEach(suggestion => {
        const button = document.createElement('button');
        button.className = 'prompt-btn';
        button.textContent = suggestion;
        button.addEventListener('click', () => {
            promptInput.value = suggestion;
            promptInput.focus();
        });
        suggestionsDiv.appendChild(button);
    });
    
    messageContent.appendChild(welcomeP);
    messageContent.appendChild(suggestionP);
    messageContent.appendChild(suggestionsDiv);
    systemMessage.appendChild(messageContent);
    
    conversationContainer.appendChild(systemMessage);
    
    // Actualizar historial
    updateHistoryList();
}

// Actualizar lista de historial
function updateHistoryList() {
    historyList.innerHTML = '';
    
    if (conversation.length > 0) {
        const date = new Date();
        const formattedDate = date.toLocaleDateString();
        const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const historyItem = document.createElement('li');
        historyItem.textContent = `Conversación ${formattedDate} ${timeStr}`;
        historyItem.addEventListener('click', () => {
            loadConversation();
        });
        
        historyList.appendChild(historyItem);
    } else {
        const emptyItem = document.createElement('li');
        emptyItem.textContent = 'No hay conversaciones guardadas';
        emptyItem.style.opacity = '0.7';
        historyList.appendChild(emptyItem);
    }
}

// Obtener información del modelo
async function fetchModelInfo() {
    try {
        const response = await fetch(`${API_URL}/model-info`);
        if (response.ok) {
            const data = await response.json();
            
            if (data.is_loaded) {
                modelStatus.innerHTML = `
                    <span style="color: var(--success-color);">✓</span> Modelo cargado<br>
                    Tipo: LSTM<br>
                    Vocabulario: ${data.vocabulary_size} tokens
                `;
            } else {
                modelStatus.innerHTML = `
                    <span style="color: var(--error-color);">✗</span> Error: ${data.error || 'Modelo no cargado'}<br>
                    <small>Revisa la consola para más detalles</small>
                `;
            }
        } else {
            throw new Error('Error al obtener información del modelo');
        }
    } catch (error) {
        console.error('Error:', error);
        modelStatus.innerHTML = `
            <span style="color: var(--error-color);">✗</span> Error de conexión<br>
            <small>No se pudo conectar con el servidor</small>
        `;
    }
} 