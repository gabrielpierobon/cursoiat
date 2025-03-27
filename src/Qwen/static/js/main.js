// Variables globales
let currentChatId = null;
let isProcessing = false;
let chatHistory = {};
let systemPrompt = "Eres un asistente de IA útil, respetuoso y sincero. Responde siempre de la mejor manera posible y con información precisa.";
let temperature = 0.7;
let maxTokens = 512;

// Referencias DOM
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('messages-container');
const newChatBtn = document.getElementById('new-chat-btn');
const chatList = document.getElementById('chat-list');
const currentChatTitle = document.getElementById('current-chat-title');
const systemPromptInput = document.getElementById('system-prompt');
const temperatureSlider = document.getElementById('temperature-slider');
const temperatureValue = document.getElementById('temperature-value');
const maxTokensSlider = document.getElementById('max-tokens-slider');
const maxTokensValue = document.getElementById('max-tokens-value');
const modelStatus = document.getElementById('model-status');

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Cargar la información del modelo
    fetchModelInfo();
    
    // Cargar chats anteriores del almacenamiento local
    loadChatsFromLocalStorage();
    
    // Crear un nuevo chat si no hay ninguno activo
    if (!currentChatId) {
        createNewChat();
    }
    
    // Configurar event listeners
    setupEventListeners();
    
    // Foco inicial en el input
    userInput.focus();
});

function setupEventListeners() {
    // Formulario de chat
    chatForm.addEventListener('submit', handleChatSubmit);
    
    // Input dinámico
    userInput.addEventListener('input', () => {
        // Ajustar altura automáticamente
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
        
        // Habilitar/deshabilitar botón de envío
        sendBtn.disabled = userInput.value.trim() === '' || isProcessing;
    });
    
    // Tecla Enter para enviar (pero permitir Shift+Enter para nueva línea)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // Botón de nuevo chat
    newChatBtn.addEventListener('click', createNewChat);
    
    // Actualizar configuración desde controles
    systemPromptInput.addEventListener('input', () => {
        systemPrompt = systemPromptInput.value;
    });
    
    temperatureSlider.addEventListener('input', () => {
        temperature = parseFloat(temperatureSlider.value);
        temperatureValue.textContent = temperature;
    });
    
    maxTokensSlider.addEventListener('input', () => {
        maxTokens = parseInt(maxTokensSlider.value);
        maxTokensValue.textContent = maxTokens;
    });
}

// Obtener información del modelo
async function fetchModelInfo() {
    try {
        const response = await fetch('/api/model_info');
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        
        const data = await response.json();
        updateModelInfo(data);
    } catch (error) {
        console.error('Error al obtener información del modelo:', error);
        modelStatus.textContent = 'Error al conectar con el modelo';
    }
}

// Actualizar información del modelo en la interfaz
function updateModelInfo(info) {
    const statusText = `Modelo: ${info.model_name}\nEstado: ${info.status}\nParámetros: ${info.parameters}\nContexto: ${formatContextLength(info.context_length)}\nDispositivo: ${info.device}`;
    modelStatus.textContent = statusText;
}

// Formatear longitud de contexto
function formatContextLength(length) {
    if (length >= 1000) {
        return `${(length / 1000).toFixed(0)}K tokens`;
    }
    return `${length} tokens`;
}

// Crear un nuevo chat
function createNewChat() {
    // Generar ID único
    const chatId = 'chat_' + Date.now();
    
    // Crear objeto de chat
    chatHistory[chatId] = {
        id: chatId,
        title: 'Nueva conversación',
        messages: [],
        systemPrompt: systemPrompt,
        created: new Date().toISOString()
    };
    
    // Establecer como chat actual
    setActiveChat(chatId);
    
    // Limpiar mensajes
    messagesContainer.innerHTML = '';
    
    // Añadir mensaje de bienvenida
    const welcomeMessage = document.createElement('div');
    welcomeMessage.className = 'welcome-message';
    welcomeMessage.innerHTML = `
        <h3>Bienvenido a Qwen Chat</h3>
        <p>Estoy listo para ayudarte. ¿Sobre qué te gustaría hablar?</p>
    `;
    messagesContainer.appendChild(welcomeMessage);
    
    // Guardar en localStorage
    saveChatsToLocalStorage();
    
    // Actualizar UI
    updateChatList();
    updateChatTitle('Nueva conversación');
    
    // Foco en input
    userInput.focus();
}

// Establecer chat activo
function setActiveChat(chatId) {
    // Actualizar ID actual
    currentChatId = chatId;
    
    // Actualizar UI
    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.id === chatId) {
            item.classList.add('active');
        }
    });
}

// Actualizar título del chat actual
function updateChatTitle(title) {
    if (currentChatId && chatHistory[currentChatId]) {
        chatHistory[currentChatId].title = title;
        currentChatTitle.textContent = title;
        
        // También actualizar en la lista de chats
        const chatItem = document.querySelector(`.chat-item[data-id="${currentChatId}"] .chat-title`);
        if (chatItem) {
            chatItem.textContent = title;
        }
        
        // Guardar cambios
        saveChatsToLocalStorage();
    }
}

// Actualizar la lista de chats en la UI
function updateChatList() {
    // Limpiar lista actual
    chatList.innerHTML = '';
    
    // Si no hay chats, mostrar mensaje
    if (Object.keys(chatHistory).length === 0) {
        const noChatsMessage = document.createElement('div');
        noChatsMessage.className = 'no-chats-message';
        noChatsMessage.textContent = 'No hay conversaciones recientes';
        chatList.appendChild(noChatsMessage);
        return;
    }
    
    // Obtener chats ordenados por fecha de creación
    const sortedChats = Object.values(chatHistory).sort((a, b) => 
        new Date(b.created) - new Date(a.created)
    );
    
    // Añadir cada chat a la lista
    sortedChats.forEach(chat => {
        const template = document.getElementById('chat-item-template');
        const chatItem = template.content.cloneNode(true).querySelector('.chat-item');
        
        chatItem.dataset.id = chat.id;
        if (chat.id === currentChatId) {
            chatItem.classList.add('active');
        }
        
        const chatTitle = chatItem.querySelector('.chat-title');
        chatTitle.textContent = chat.title;
        
        // Evento de clic para cargar el chat
        chatItem.addEventListener('click', () => loadChat(chat.id));
        
        // Botón de eliminar chat
        const deleteBtn = chatItem.querySelector('.delete-chat-btn');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteChat(chat.id);
        });
        
        chatList.appendChild(chatItem);
    });
}

// Cargar un chat existente
function loadChat(chatId) {
    if (!chatHistory[chatId]) return;
    
    // Establecer como chat activo
    setActiveChat(chatId);
    
    // Actualizar título
    updateChatTitle(chatHistory[chatId].title);
    
    // Limpiar mensajes anteriores
    messagesContainer.innerHTML = '';
    
    // Cargar mensajes del chat
    const messages = chatHistory[chatId].messages;
    
    if (messages.length === 0) {
        // Si no hay mensajes, mostrar bienvenida
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'welcome-message';
        welcomeMessage.innerHTML = `
            <h3>Bienvenido a Qwen Chat</h3>
            <p>Estoy listo para ayudarte. ¿Sobre qué te gustaría hablar?</p>
        `;
        messagesContainer.appendChild(welcomeMessage);
    } else {
        // Renderizar mensajes existentes
        messages.forEach(msg => {
            if (msg.role === 'user') {
                addUserMessage(msg.content, new Date(msg.timestamp));
            } else if (msg.role === 'assistant') {
                addBotMessage(msg.content, msg.metadata, new Date(msg.timestamp));
            }
        });
    }
    
    // Actualizar sistema prompt en la interfaz
    systemPromptInput.value = chatHistory[chatId].systemPrompt || systemPrompt;
    systemPrompt = systemPromptInput.value;
    
    // Scroll al final
    scrollToBottom();
    
    // Foco en input
    userInput.focus();
}

// Eliminar un chat
function deleteChat(chatId) {
    // Confirmación
    if (!confirm('¿Estás seguro de que deseas eliminar esta conversación?')) {
        return;
    }
    
    // Eliminar chat del historial
    delete chatHistory[chatId];
    
    // Si era el chat actual, crear uno nuevo
    if (chatId === currentChatId) {
        // Si hay otros chats, cargar el primero
        const remainingChats = Object.keys(chatHistory);
        if (remainingChats.length > 0) {
            loadChat(remainingChats[0]);
        } else {
            createNewChat();
        }
    }
    
    // Guardar cambios
    saveChatsToLocalStorage();
    
    // Actualizar UI
    updateChatList();
}

// Manejar envío de mensaje
async function handleChatSubmit(e) {
    e.preventDefault();
    
    if (isProcessing) return;
    
    const userMessage = userInput.value.trim();
    if (!userMessage) return;
    
    // Actualizar estado
    isProcessing = true;
    sendBtn.disabled = true;
    
    // Añadir mensaje a la UI
    addUserMessage(userMessage);
    
    // Limpiar input y restaurar altura
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Añadir mensaje al historial del chat
    if (currentChatId && chatHistory[currentChatId]) {
        chatHistory[currentChatId].messages.push({
            role: 'user',
            content: userMessage,
            timestamp: new Date().toISOString()
        });
        
        // Si es el primer mensaje, actualizar título
        if (chatHistory[currentChatId].messages.length === 1) {
            const chatTitle = generateChatTitle(userMessage);
            updateChatTitle(chatTitle);
        }
        
        // Guardar cambios
        saveChatsToLocalStorage();
    }
    
    // Mostrar indicador de "pensando"
    const thinkingElement = addThinkingIndicator();
    
    try {
        // Preparar mensajes para la API
        const messages = [];
        
        // Añadir prompt del sistema
        messages.push({
            role: 'system',
            content: systemPrompt
        });
        
        // Añadir historial de mensajes
        if (currentChatId && chatHistory[currentChatId]) {
            chatHistory[currentChatId].messages.forEach(msg => {
                if (msg.role === 'user' || msg.role === 'assistant') {
                    messages.push({
                        role: msg.role,
                        content: msg.content
                    });
                }
            });
        }
        
        // Llamar a la API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: messages,
                system_prompt: systemPrompt,
                temperature: temperature,
                max_tokens: maxTokens
            }),
        });
        
        // Verificar respuesta
        if (!response.ok) {
            throw new Error('Error en la respuesta de la API');
        }
        
        // Procesar respuesta
        const data = await response.json();
        
        // Eliminar indicador de pensando
        thinkingElement.remove();
        
        // Verificar éxito
        if (!data.success) {
            throw new Error(data.error || 'Error al generar respuesta');
        }
        
        // Añadir respuesta a la UI
        const metadata = {
            time: data.time,
            tokens: data.tokens
        };
        addBotMessage(data.response, metadata);
        
        // Añadir respuesta al historial
        if (currentChatId && chatHistory[currentChatId]) {
            chatHistory[currentChatId].messages.push({
                role: 'assistant',
                content: data.response,
                metadata: metadata,
                timestamp: new Date().toISOString()
            });
            
            // Guardar cambios
            saveChatsToLocalStorage();
        }
        
    } catch (error) {
        console.error('Error:', error);
        
        // Eliminar indicador de pensando
        thinkingElement.remove();
        
        // Mostrar error en la UI
        addErrorMessage(error.message || 'Se ha producido un error al procesar tu solicitud.');
    } finally {
        // Restaurar estado
        isProcessing = false;
        sendBtn.disabled = false;
        
        // Foco en input
        userInput.focus();
    }
}

// Añadir mensaje del usuario a la UI
function addUserMessage(content, timestamp = new Date()) {
    // Eliminar mensaje de bienvenida si existe
    const welcomeMessage = messagesContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    // Crear elemento de mensaje
    const template = document.getElementById('user-message-template');
    const messageElement = template.content.cloneNode(true);
    
    // Rellenar contenido
    messageElement.querySelector('.message-content').textContent = content;
    messageElement.querySelector('.message-timestamp').textContent = formatTimestamp(timestamp);
    
    // Añadir a la UI
    messagesContainer.appendChild(messageElement);
    
    // Scroll al final
    scrollToBottom();
}

// Añadir mensaje del bot a la UI
function addBotMessage(content, metadata = {}, timestamp = new Date()) {
    // Crear elemento de mensaje
    const template = document.getElementById('bot-message-template');
    const messageElement = template.content.cloneNode(true);
    
    // Rellenar contenido
    messageElement.querySelector('.message-content').textContent = content;
    messageElement.querySelector('.message-timestamp').textContent = formatTimestamp(timestamp);
    
    // Formatear y añadir metadatos
    let metricsText = '';
    if (metadata.tokens) metricsText += `${metadata.tokens} tokens`;
    if (metadata.time) {
        if (metricsText) metricsText += ' · ';
        metricsText += `${metadata.time.toFixed(2)}s`;
    }
    messageElement.querySelector('.message-metrics').textContent = metricsText;
    
    // Configurar botón de copia
    const copyBtn = messageElement.querySelector('.copy-btn');
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(content)
            .then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
    });
    
    // Añadir a la UI
    messagesContainer.appendChild(messageElement);
    
    // Scroll al final
    scrollToBottom();
}

// Añadir mensaje de error a la UI
function addErrorMessage(content) {
    // Crear elemento de mensaje
    const template = document.getElementById('error-message-template');
    const messageElement = template.content.cloneNode(true);
    
    // Rellenar contenido
    messageElement.querySelector('.message-content').textContent = content;
    
    // Añadir a la UI
    messagesContainer.appendChild(messageElement);
    
    // Scroll al final
    scrollToBottom();
}

// Añadir indicador de "pensando"
function addThinkingIndicator() {
    // Crear elemento
    const template = document.getElementById('thinking-template');
    const thinkingElement = template.content.cloneNode(true);
    
    // Añadir a la UI
    messagesContainer.appendChild(thinkingElement);
    
    // Scroll al final
    scrollToBottom();
    
    // Retornar el elemento para poder eliminarlo después
    return messagesContainer.lastElementChild;
}

// Scroll al final del contenedor de mensajes
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Formatear timestamp
function formatTimestamp(date) {
    const now = new Date();
    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1);
    
    // Mismo día
    if (date.toDateString() === now.toDateString()) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    // Ayer
    else if (date.toDateString() === yesterday.toDateString()) {
        return 'Ayer ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    // Otro día
    else {
        return date.toLocaleDateString([], { day: '2-digit', month: '2-digit', year: '2-digit' }) + ' ' + 
               date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
}

// Generar título de chat a partir del primer mensaje
function generateChatTitle(message) {
    // Limitar a 30 caracteres más puntos suspensivos si es necesario
    return message.length > 30 ? message.substring(0, 30) + '...' : message;
}

// Guardar chats en localStorage
function saveChatsToLocalStorage() {
    try {
        localStorage.setItem('qwen_chat_history', JSON.stringify(chatHistory));
    } catch (error) {
        console.error('Error al guardar chats en localStorage:', error);
    }
}

// Cargar chats desde localStorage
function loadChatsFromLocalStorage() {
    try {
        const saved = localStorage.getItem('qwen_chat_history');
        if (saved) {
            chatHistory = JSON.parse(saved);
            
            // Verificar si hay un chat activo guardado
            const lastActiveChatId = localStorage.getItem('qwen_active_chat_id');
            if (lastActiveChatId && chatHistory[lastActiveChatId]) {
                currentChatId = lastActiveChatId;
                // Cargar el chat
                setTimeout(() => loadChat(currentChatId), 0);
            }
            
            // Actualizar UI
            updateChatList();
        }
    } catch (error) {
        console.error('Error al cargar chats desde localStorage:', error);
        // Si hay error, reiniciar
        chatHistory = {};
    }
} 