# DocAssist Academic

## Descripción General
DocAssist Academic es una aplicación web que permite a estudiantes y académicos automatizar el análisis de documentos educativos (PDF) mediante inteligencia artificial. Utiliza modelos pre-entrenados  "GPT 3.5 Turbo " en español en Azure para generar resúmenes ejecutivos y responder preguntas clave sobre el contenido, optimizando el estudio y la investigación.

## Problema que Resuelve
El análisis de documentos académicos es una tarea fundamental pero que consume mucho tiempo. DocAssist Academic surge como respuesta a esta necesidad, proporcionando una solución tecnológica que aprovecha las capacidades de la inteligencia artificial para automatizar y optimizar el proceso de análisis documental.

## Características Principales
- **Resúmenes Ejecutivos**: Generación automática de resúmenes concisos que capturan la esencia del documento
- **Consultas Interactivas**: Capacidad para realizar preguntas específicas sobre el contenido y obtener respuestas precisas
- **Interfaz Intuitiva**: Experiencia de usuario simple y accesible
- **Soporte para PDF**: Procesamiento de documentos académicos en formato PDF


## Tecnologías Utilizadas
- **Backend**: Python 3.11, Flask
- **Procesamiento de Lenguaje Natural**: Azure OpenAI Service (GPT 3.5 Turbo)
- **Almacenamiento**: Azure Blob Storage
- **Despliegue**: Azure Web App Service
- **Control de Versiones**: Git/GitHub

## Arquitectura
El sistema se basa en microservicios desplegados en Azure:
- **Capa de Presentación**: Interfaz web desarrollada con Flask
- **Capa de Lógica**: Servicios de procesamiento y análisis de documentos
- **Capa de Almacenamiento**: Azure Blob Storage para documentos
- **Capa de IA**: Azure OpenAI Service para procesamiento de lenguaje natural

## Requisitos Previos
- Python 3.11 o superior
- Cuenta de Azure con suscripción activa
- Recursos aprovisionados en Azure:
  - Azure Blob Storage
  - Azure OpenAI Service con modelo GPT 3.5 Turbo
  - Azure Web App Service (para despliegue)

## Instalación y Configuración

### Configuración Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/daplaza82/DocAssist.git
   cd DocAssist
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crear un archivo `.env` en la raíz del proyecto con la siguiente información:
   ```
   AZURE_STORAGE_CONNECTION_STRING=your_connection_string
   AZURE_AI_ENDPOINT=your_endpoint
   AZURE_AI_KEY=your_key
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

5. **Ejecutar la aplicación localmente**
   ```bash
   flask run
   ```
   La aplicación estará disponible en `http://localhost:5000`

## Uso

### Interfaz Web

1. **Inicio de Sesión**
   - Acceder a la aplicación web

2. **Carga de Documentos**
   - Hacer clic en "Seleccionar Archivo"
   - Seleccionar un archivo PDF de contenido académico
   - Hacer clic en "Analizar Documento"
   - Esperar a que se complete el procesamiento

3. **Análisis del Documento**
   - Visualizar el resumen ejecutivo generado automáticamente
   - Utilizar la sección de consultas para hacer preguntas específicas


## Estructura del Proyecto

```
DocAssist/
│
├── app/                       # Contiene la lógica principal de la aplicación
│   ├── __init__.py            # Inicializa la aplicación como un paquete de Python
│   ├── main.py                # (API) Archivo principal de la aplicación
│   ├── templates/             # Almacena las plantillas HTML para la interfaz de usuario
│   │   ├── base.html          # Plantilla base que contiene elementos comunes (header, footer, estilos). 
│   │   └── index.html         # Página principal donde los usuarios pueden cargar documentos y ver los resultados del análisis
│   └── static/                # Contiene archivos estáticos como estilos CSS y scripts JavaScript.
│       ├── css/               # Contiene archivos estáticos como estilos CSS y scripts JavaScript.
│       │   └── styles.css     # Define los estilos de la interfaz de usuario.
│       └── js/                #  Contine los archivos JavaScript
│           └── app.js         # Contiene scripts de JavaScript para interactividad
│
├── .env                       # Archivo para almacenar variables de entorno claves de API de Azure y configuraciones sensibles
├── .gitignore                 # Lista de archivos que Git debe ignorar (como .env y cachés).
├── requirements.txt           # Lista de dependencias de Python necesarias para ejecutar la aplicación
└── run.py                     # Archivo para iniciar la aplicación. Importa main.py y ejecuta el servidor Flask
```

## Solución de Problemas

### Problemas Comunes

1. **Error de Conexión a Azure**
   - Verificar las cadenas de conexión en el archivo `.env`
   - Comprobar que los recursos estén activos en el portal de Azure
   - Revisar la configuración de firewall y CORS

2. **Errores en el Procesamiento de PDF**
   - Asegurarse de que el PDF no esté protegido o dañado
   - Verificar que el contenido sea texto seleccionable y no imágenes

3. **Respuestas Incorrectas del Modelo**
   - Ajustar los prompts en la configuración del modelo
   - Considerar el uso de modelos más avanzados para contenido complejo

## Licencia

Este proyecto está licenciado bajo [Especificar Licencia]

## Contacto

[David Plaza] - [daplaza82@gmail.com]

Enlace del Proyecto: [https://github.com/daplaza82/DocAssist](https://github.com/daplaza82/DocAssist)
