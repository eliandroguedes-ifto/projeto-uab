from app import db, cache
from app.models import Usuario, Solicitacao
from flask_bcrypt import Bcrypt
from datetime import datetime
import threading

bcrypt = Bcrypt()

# --- Auth Service ---
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

# --- Ticket Service ---
def criar_solicitacao(cliente_id, assunto, descricao):
    nova_solicitacao = Solicitacao(cliente_id=cliente_id, assunto=assunto, descricao=descricao)
    db.session.add(nova_solicitacao)
    db.session.commit()
    
    # Limpa o cache de estatísticas pois um novo chamado foi criado
    cache.delete('admin_stats')
    
    # Simula um Job em Background (Fila)
    threading.Thread(target=_job_notificar_criacao, args=(nova_solicitacao.id,)).start()
    
    return nova_solicitacao

def responder_solicitacao(solicitacao_id, resposta, novo_status):
    solicitacao = db.session.get(Solicitacao, solicitacao_id)
    if solicitacao:
        solicitacao.resposta_atendente = resposta
        solicitacao.status = novo_status
        db.session.commit()
        
        # Limpa o cache de estatísticas
        cache.delete('admin_stats')
        
        # Simula Job em Background
        threading.Thread(target=_job_notificar_resposta, args=(solicitacao_id,)).start()
        
        return solicitacao
    return None

def buscar_solicitacao_por_id(solicitacao_id):
    return db.session.get(Solicitacao, solicitacao_id)

def listar_solicitacoes_cliente(cliente_id):
    return Solicitacao.query.filter_by(cliente_id=cliente_id).order_by(Solicitacao.data_criacao.desc()).all()

def listar_fila_atendimento():
    return Solicitacao.query.filter(Solicitacao.status.in_(['ABERTO', 'EM_ANDAMENTO'])).order_by(Solicitacao.data_criacao.asc()).all()

# --- Admin Service (com Cache) ---
@cache.cached(timeout=300, key_prefix='admin_stats')
def obter_estatisticas_admin():
    total = Solicitacao.query.count()
    abertos = Solicitacao.query.filter_by(status='ABERTO').count()
    em_andamento = Solicitacao.query.filter_by(status='EM_ANDAMENTO').count()
    resolvidos = Solicitacao.query.filter_by(status='RESOLVIDO').count()
    
    recentes = Solicitacao.query.order_by(Solicitacao.data_criacao.desc()).limit(10).all()
    
    return {
        'total': total,
        'abertos': abertos,
        'em_andamento': em_andamento,
        'resolvidos': resolvidos,
        'recentes': recentes
    }

# --- Background Jobs (Private) ---
def _job_notificar_criacao(solicitacao_id):
    """Simula o processamento de um job em fila para notificação."""
    print(f"[JOB] Notificando criação da solicitação #{solicitacao_id}")
    # Aqui poderia haver envio de email ou integração externa

def _job_notificar_resposta(solicitacao_id):
    """Simula o processamento de um job em fila para resposta."""
    print(f"[JOB] Notificando resposta para solicitação #{solicitacao_id}")
