from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Crear instancias globales
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mi_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import Usuario  # Importa después de init_app
    from app.routes import main
    app.register_blueprint(main)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app

# Para que sea accesible desde otros módulos
__all__ = ['create_app', 'db']
