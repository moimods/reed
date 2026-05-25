/**
 * Script del Analizador Léxico
 * Maneja interacción con el backend, renderizado de tokens y syntax highlighting
 */

// ============================================
// ELEMENTOS DEL DOM
// ============================================

const codeInput = document.getElementById('codeInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const tableBody = document.getElementById('tableBody');
const tokenCount = document.getElementById('tokenCount');
const errorList = document.getElementById('errorList');
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');
const syntaxPreview = document.getElementById('syntaxPreview');
const treeFrame = document.getElementById('treeFrame');

// ============================================
// CONFIGURACIÓN Y CONSTANTES
// ============================================

const TOKEN_COLORS = {
    'PALABRA_RESERVADA': '#ec4899',
    'VARIABLE': '#3b82f6',
    'ENTERO': '#10b981',
    'OPERADOR': '#f59e0b',
    'CARACTER_ESPECIAL': '#8b5cf6',
    'SALTO_LINEA': '#64748b',
    'ERROR': '#ef4444',
    'ESPACIO': '#cbd5e1'
};

const TOKEN_DISPLAY = {
    PALABRA_RESERVADA: 'palabra reservada',
    IDENTIFICADOR: 'variable',
    ENTERO: 'integer',
    FLOAT: 'float',
    STRING: 'string',
    OPERADOR: 'operador',
    CARACTER_ESPECIAL: 'caracter especial',
    COMENTARIO: 'comentario',
    SALTO_LINEA: 'salto de linea',
    ESPACIO: 'espacio vacio',
    BOOLEANO: 'booleano',
    NULL: 'null',
    ERROR: 'error'
};

function getDisplayType(tipo) {
    return TOKEN_DISPLAY[tipo] || tipo.toLowerCase();
}

function getVisualType(tipo) {
    if (tipo === 'IDENTIFICADOR') return 'VARIABLE';
    return tipo;
}

function getTokenDisplayValue(token) {
    if (token.tipo === 'SALTO_LINEA') {
        return '/n';
    }

    if (token.tipo === 'ESPACIO') {
        if (/^\t+$/.test(token.valor)) {
            return '/t';
        }
        return token.valor;
    }

    return token.valor;
}

// ============================================
// EVENT LISTENERS
// ============================================

analyzeBtn.addEventListener('click', analyzeCode);
clearBtn.addEventListener('click', clearAll);

// Event listeners para tabs
tabButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const tabName = e.target.getAttribute('data-tab');
        switchTab(tabName);
    });
});

// Auto-analyze en tiempo real (opcional - comentado para economizar requests)
// codeInput.addEventListener('input', debounce(analyzeCode, 500));

// ============================================
// FUNCIÓN PRINCIPAL: ANALIZAR CÓDIGO
// ============================================

async function analyzeCode() {
    const codigo = codeInput.value;

    if (!codigo.trim()) {
        showNotification('Por favor, escribe código para analizar', 'warning');
        return;
    }

    // Mostrar estado de carga
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analizando...';

    try {
        // Enviar código al backend
        const response = await fetch('/analyze/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                codigo: codigo,
                lenguaje: 'python'
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Respuesta no OK del backend:', response.status, errorText);
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log('Tokens recibidos del backend:', data.tokens);
        console.log('Respuesta completa:', data);

        // Procesar y mostrar resultados
        displayResults(data);

    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
        console.error('Error al analizar:', error);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analizar';
    }
}

function getCSRFToken() {
    const cookieToken = getCookie('csrftoken');
    if (cookieToken) {
        return cookieToken;
    }

    const formTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (formTokenInput && formTokenInput.value) {
        return formTokenInput.value;
    }

    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken && metaToken.getAttribute('content')) {
        return metaToken.getAttribute('content');
    }

    return '';
}

// ============================================
// MOSTRAR RESULTADOS
// ============================================

function displayResults(data) {
    const { tokens, errores, total_tokens } = data;

    // Mostrar sección de resultados
    resultsSection.classList.remove('hidden');
    tokenCount.textContent = `Total: ${total_tokens} tokens`;

    // Mostrar/ocultar sección de errores
    if (errores.length > 0) {
        errorSection.classList.remove('hidden');
        displayErrors(errores);
    } else {
        errorSection.classList.add('hidden');
    }

    // Renderizar tabla de tokens
    renderTokensTable(tokens);

    // Renderizar preview con syntax highlighting
    renderSyntaxPreview(tokens);

    // Cargar el módulo del árbol con el mismo código del analizador
    treeFrame.src = `/arbol/?codigo=${encodeURIComponent(codeInput.value)}&lenguaje=python`;

    // Scroll a resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================
// RENDERIZAR TABLA DE TOKENS
// ============================================

function renderTokensTable(tokens) {
    tableBody.innerHTML = '';

    tokens.forEach((token, index) => {
        const row = document.createElement('tr');

        // Columna: Número
        const tdNum = document.createElement('td');
        tdNum.textContent = index + 1;
        row.appendChild(tdNum);

        // Columna: Token formateado como <'valor', tipo>
        const tdToken = document.createElement('td');
        const spanToken = document.createElement('span');
        spanToken.className = `token-tipo ${getVisualType(token.tipo)}`;
        const displayValue = getTokenDisplayValue(token);
        const displayType = getDisplayType(token.tipo);
        spanToken.textContent = `<'${displayValue}', ${displayType}>`;
        tdToken.appendChild(spanToken);
        row.appendChild(tdToken);

        tableBody.appendChild(row);
    });
}

// ============================================
// RENDERIZAR PREVIEW CON SYNTAX HIGHLIGHTING
// ============================================

function renderSyntaxPreview(tokens) {
    syntaxPreview.innerHTML = '';

    let currentLinea = 1;
    let lineDiv = document.createElement('div');
    
    tokens.forEach(token => {
        // Crear nueva línea si es necesario
        if (token.linea !== currentLinea) {
            syntaxPreview.appendChild(lineDiv);
            for (let i = currentLinea; i < token.linea; i++) {
                const newLineDiv = document.createElement('div');
                syntaxPreview.appendChild(newLineDiv);
            }
            lineDiv = document.createElement('div');
            currentLinea = token.linea;
        }

        // Crear span para el token
        const span = document.createElement('span');
        span.className = `token-span ${getVisualType(token.tipo)}`;
        
        if (token.tipo === 'SALTO_LINEA') {
            span.textContent = '\n';
        } else {
            span.textContent = token.valor;
        }

        lineDiv.appendChild(span);
    });

    // Agregar la última línea
    if (lineDiv.children.length > 0) {
        syntaxPreview.appendChild(lineDiv);
    }
}

// ============================================
// MOSTRAR ERRORES LÉXICOS
// ============================================

function displayErrors(errores) {
    errorList.innerHTML = '';

    errores.forEach(error => {
        const errorItem = document.createElement('div');
        errorItem.className = 'error-item';
        errorItem.textContent = error;
        errorList.appendChild(errorItem);
    });
}

// ============================================
// MANEJO DE TABS
// ============================================

function switchTab(tabName) {
    // Desactivar todos los tabs
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));

    // Activar el tab seleccionado
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

// ============================================
// LIMPIAR TODO
// ============================================

function clearAll() {
    codeInput.value = '';
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    tableBody.innerHTML = '';
    errorList.innerHTML = '';
    syntaxPreview.innerHTML = '';
    treeFrame.src = 'about:blank';
    
    codeInput.focus();
}

// ============================================
// UTILIDADES
// ============================================

/**
 * Obtener token CSRF de Django
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Debounce para ejecución demorada
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

/**
 * Mostrar notificación (sin librería externa)
 */
function showNotification(message, type = 'info') {
    // Crear elemento temporal (en un proyecto real, usar librería)
    const notif = document.createElement('div');
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        font-weight: 600;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        ${type === 'error' ? 'background: #ef4444; color: white;' : ''}
        ${type === 'warning' ? 'background: #f59e0b; color: white;' : ''}
        ${type === 'success' ? 'background: #10b981; color: white;' : ''}
        ${type === 'info' ? 'background: #2563eb; color: white;' : ''}
    `;
    notif.textContent = message;
    document.body.appendChild(notif);

    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// Agregar animaciones al CSS dinámicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// INICIALIZACIÓN
// ============================================

// Focus en el textarea al cargar
document.addEventListener('DOMContentLoaded', () => {
    codeInput.focus();
});
