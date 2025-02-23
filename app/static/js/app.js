// Variables globales
let documentText = ''; // Almacena el texto del documento para preguntas

// Función para mostrar alertas
function showAlert(message, type = 'error') {
    const alertContainer = document.getElementById('alert-container');
    const alertMessage = document.getElementById('alert-message');
    const alertDiv = alertContainer.querySelector('div');
    const iconSvg = alertContainer.querySelector('.alert-icon svg');
    
    // Configurar estilos según el tipo
    if (type === 'error') {
        alertDiv.className = 'relative p-4 rounded-lg shadow-lg border-l-4 border-red-500 bg-red-50 text-red-800 transform transition-all duration-500 ease-in-out';
        iconSvg.innerHTML = `
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        `;
    } else {
        alertDiv.className = 'relative p-4 rounded-lg shadow-lg border-l-4 border-green-500 bg-green-50 text-green-800 transform transition-all duration-500 ease-in-out';
        iconSvg.innerHTML = `
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        `;
    }
    
    // Establecer mensaje
    alertMessage.textContent = message;
    
    // Mostrar alerta con animación
    alertContainer.classList.remove('hidden');
    alertDiv.style.transform = 'translateX(0)';
    alertDiv.style.opacity = '1';
    
    // Ocultar después de 5 segundos
    setTimeout(() => {
        alertDiv.style.transform = 'translateX(100%)';
        alertDiv.style.opacity = '0';
        setTimeout(() => {
            alertContainer.classList.add('hidden');
        }, 500);
    }, 5000);
}

// Función para mostrar/ocultar el indicador de carga
function toggleLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

// Función para mostrar resultados
function displayResults(data) {
    const resultsSection = document.getElementById('results-section');
    const summary = document.getElementById('summary');
    const keyPoints = document.getElementById('key-points');

    summary.textContent = data.summary;
    keyPoints.textContent = data.key_points;
    documentText = data.text; // Guardar para preguntas posteriores
    
    resultsSection.classList.remove('hidden');
}

// Procesar el documento
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Por favor selecciona un archivo PDF');
        return;
    }
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showAlert('Solo se permiten archivos PDF');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        toggleLoading(true);
        
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        displayResults(result);
        showAlert('Documento analizado exitosamente', 'success');
        
    } catch (error) {
        showAlert(error.message || 'Error al procesar el documento');
        console.error('Error:', error);
    } finally {
        toggleLoading(false);
    }
});

// Función para hacer preguntas
async function askQuestion() {
    const questionInput = document.getElementById('question-input');
    const question = questionInput.value.trim();
    const answerContainer = document.getElementById('answer-container');
    const answerElement = document.getElementById('answer');
    
    if (!question) {
        showAlert('Por favor escribe una pregunta');
        return;
    }

    if (!documentText) {
        showAlert('Primero debes analizar un documento');
        return;
    }

    try {
        toggleLoading(true);
        
        const response = await fetch('/question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                text: documentText
            })
        });

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        answerElement.textContent = result.answer;
        answerContainer.classList.remove('hidden');
        
    } catch (error) {
        showAlert(error.message || 'Error al procesar la pregunta');
        console.error('Error:', error);
    } finally {
        toggleLoading(false);
    }
}

// Event listener para el botón de preguntas
document.addEventListener('DOMContentLoaded', () => {
    const questionInput = document.getElementById('question-input');
    
    // Permitir enviar pregunta con Enter
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            askQuestion();
        }
    });
});