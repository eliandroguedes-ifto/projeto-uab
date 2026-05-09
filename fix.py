from app import create_app, db, bcrypt
from app.models import Usuario

app = create_app()
with app.app_context():
     Usuario.query.filter_by(email='admin@sistema.com').delete()
     db.session.commit()
     h = bcrypt.generate_password_hash('SenhaAdmin123!').decode('utf-8')
     admin = Usuario(nome='Admin', email='admin@sistema.com', senha_hash=h, perfil='ADMIN')
     db.session.add(admin)
     db.session.commit()
     print('--- SUCESSO: ADMIN RESETADO ---')
