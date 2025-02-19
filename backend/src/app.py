import os
from flask import Flask
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads
from routes import Carro, Review, Usuario
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuración de Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

app = Flask(__name__)

# Configuración de Flask-Uploads
app.config['UPLOADED_FILES_DEST'] = 'StudentsLists'
files = UploadSet('files', ('pdf', 'docx', 'csv', 'xlsx', 'xls'))
configure_uploads(app, files)

def get_uploads_set():
    return files

CORS(app, resources={"*": {"origins": "*"}})

def page_not_found(error):
    return "Page not found", 404

# Cargar configuración desde variables de entorno
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersupersecreto')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

if __name__ == '__main__':
    # Blueprints
    app.register_blueprint(Carro.carro_bp, url_prefix='/api/carros')
    app.register_blueprint(Review.review_bp, url_prefix='/api/reviews')
    app.register_blueprint(Usuario.usuario_bp, url_prefix='/api/usuarios')

    # Error handling
    app.register_error_handler(404, page_not_found)

    # Definir el puerto desde variables de entorno o usar 5000 por defecto
    PORT = int(os.getenv('PORT', 5000))

    app.run(host='0.0.0.0', port=PORT)
