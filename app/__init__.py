from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-secreta-padrao')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///../instance/database.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from app import models # Importar models para que db.create_all() funcione
        db.create_all() # Cria o arquivo SQLite e as tabelas se não existirem

        # Rotina de Seed do Administrador
        admin_email = os.getenv('ADMIN_INITIAL_EMAIL')
        admin_password = os.getenv('ADMIN_INITIAL_PASSWORD')

        if admin_email and admin_password and not models.Usuario.query.filter_by(email=admin_email).first():
            hash_senha_admin = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            usuario_admin = models.Usuario(nome="Administrador", email=admin_email, senha_hash=hash_senha_admin, perfil='ADMIN')
            db.session.add(usuario_admin)
            db.session.commit()

    from app.routes import routes as main_routes # Renomeado para evitar conflito
    app.register_blueprint(main_routes)

    return app
