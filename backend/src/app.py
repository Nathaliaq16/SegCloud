from flask import Flask
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads
from config import config
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

if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(Carro.carro_bp, url_prefix='/api/carros')
    app.register_blueprint(Review.review_bp, url_prefix='/api/reviews')
    app.register_blueprint(Usuario.usuario_bp, url_prefix='/api/usuarios')

    # Error handling
    app.register_error_handler(404, page_not_found)

    app.run(host='0.0.0.0', port=8080)

