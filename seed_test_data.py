from app import create_app, db, bcrypt
from app.models import Usuario, Solicitacao
from datetime import datetime

app = create_app()
with app.app_context():
     # 1. Criar Atendente
     if not Usuario.query.filter_by(email='atendente@sistema.com').first():
         h = bcrypt.generate_password_hash('SenhaAtendente123!').decode('utf-8')
         atendente = Usuario(nome='Atendente Teste', email='atendente@sistema.com', senha_hash=h,
perfil='ATENDENTE')
         db.session.add(atendente)

     # 2. Criar Cliente
     cliente = Usuario.query.filter_by(email='cliente@email.com').first()
     if not cliente:
         h = bcrypt.generate_password_hash('SenhaCliente123!').decode('utf-8')
         cliente = Usuario(nome='João Cliente', email='cliente@email.com', senha_hash=h, perfil='CLIENTE')
         db.session.add(cliente)
         db.session.commit()

     # 3. Criar uma Solicitação de exemplo para o cliente
     if not Solicitacao.query.filter_by(cliente_id=cliente.id).first():
         nova_s = Solicitacao(
             cliente_id=cliente.id,
             assunto='Problema no Acesso',
             descricao='Não consigo acessar minha fatura mensal.',
             status='ABERTO'
         )
         db.session.add(nova_s)

     db.session.commit()
     print("--- DADOS DE TESTE CRIADOS ---")
     print("Atendente: atendente@sistema.com / SenhaAtendente123!")
     print("Cliente: cliente@email.com / SenhaCliente123!")
