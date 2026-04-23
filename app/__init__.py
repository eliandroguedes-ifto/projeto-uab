from flask import Flask
import os
from dotenv import load_dotenv
from app.models import db
from app.services import bcrypt

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-secreta-padrao')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///../instance/database.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from app import models
        # Ensure the instance folder exists
        if not os.path.exists('instance'):
            os.makedirs('instance')
            
        db.create_all()

        # Seed Admin
        admin_email = os.getenv('ADMIN_INITIAL_EMAIL')
        admin_password = os.getenv('ADMIN_INITIAL_PASSWORD')

        if admin_email and admin_password and not models.Usuario.query.filter_by(email=admin_email).first():
            hash_senha_admin = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            usuario_admin = models.Usuario(nome="Administrador", email=admin_email, senha_hash=hash_senha_admin, perfil='ADMIN')
            db.session.add(usuario_admin)
            db.session.commit()

    from app.routes import routes as main_routes
    app.register_blueprint(main_routes)

    return app
