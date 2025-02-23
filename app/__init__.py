from flask import Flask
from dotenv import load_dotenv
import os
import openai
from azure.storage.blob import BlobServiceClient

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configurar Azure Blob Storage
    app.config['BLOB_SERVICE_CLIENT'] = BlobServiceClient.from_connection_string(
        os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    )
    
    # Configurar OpenAI
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_AI_ENDPOINT")
    openai.api_version = "2023-05-15"
    openai.api_key = os.getenv("AZURE_AI_KEY")
    
    # Registrar las rutas
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app