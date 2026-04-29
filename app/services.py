from app import db
from app.models import Usuario, Solicitacao
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

def autenticar_usuario(email_entrada, senha_entrada):
    usuario = Usuario.query.filter_by(email=email_entrada).first()
    if usuario and bcrypt.check_password_hash(usuario.senha_hash, senha_entrada):
        return usuario
    return None

def registrar_cliente(nome, email, senha_plana):
    if Usuario.query.filter_by(email=email).first():
        return "Erro: Email já em uso"
    hash_senha = bcrypt.generate_password_hash(senha_plana).decode('utf-8')
    novo_cliente = Usuario(nome=nome, email=email, senha_hash=hash_senha, perfil='CLIENTE')
    db.session.add(novo_cliente)
    db.session.commit()
    return novo_cliente

def criar_solicitacao(cliente_id, assunto, descricao):
    nova_solicitacao = Solicitacao(cliente_id=cliente_id, assunto=assunto, descricao=descricao)
    db.session.add(nova_solicitacao)
    db.session.commit()
    return nova_solicitacao

def responder_solicitacao(solicitacao_id, resposta, novo_status):
    solicitacao = Solicitacao.query.get(solicitacao_id)
    if solicitacao:
        solicitacao.resposta_atendente = resposta
        solicitacao.status = novo_status
        db.session.commit()
        return solicitacao
    return None

def obter_estatisticas_admin():
    abertos = Solicitacao.query.filter_by(status='ABERTO').count()
    em_andamento = Solicitacao.query.filter_by(status='EM_ANDAMENTO').count()
    resolvidos = Solicitacao.query.filter_by(status='RESOLVIDO').count()
    return {
        'abertos': abertos,
        'em_andamento': em_andamento,
        'resolvidos': resolvidos
    }
