import pytest
from app import db
from app.models import Usuario, Solicitacao
from app.services import registrar_cliente, autenticar_usuario, criar_solicitacao, responder_solicitacao, obter_estatisticas_admin

def test_registrar_cliente_sucesso(app):
    with app.app_context():
        cliente = registrar_cliente("Teste Cliente", "teste@email.com", "senha123")
        assert isinstance(cliente, Usuario)
        assert cliente.email == "teste@email.com"
        assert cliente.perfil == "CLIENTE"

def test_registrar_cliente_duplicado(app):
    with app.app_context():
        registrar_cliente("Teste 1", "teste@email.com", "senha123")
        erro = registrar_cliente("Teste 2", "teste@email.com", "senha456")
        assert erro == "Erro: Email já em uso"

def test_autenticar_usuario_sucesso(app):
    with app.app_context():
        registrar_cliente("Teste", "login@email.com", "senha123")
        usuario = autenticar_usuario("login@email.com", "senha123")
        assert usuario is not None
        assert usuario.email == "login@email.com"

def test_autenticar_usuario_falha(app):
    with app.app_context():
        registrar_cliente("Teste", "login@email.com", "senha123")
        usuario = autenticar_usuario("login@email.com", "senha_errada")
        assert usuario is None

def test_criar_solicitacao(app):
    with app.app_context():
        cliente = registrar_cliente("Teste", "cliente@email.com", "senha123")
        solicitacao = criar_solicitacao(cliente.id, "Assunto Teste", "Descricao Teste")
        assert solicitacao.id is not None
        assert solicitacao.assunto == "Assunto Teste"
        assert solicitacao.status == "ABERTO"

def test_responder_solicitacao(app):
    with app.app_context():
        cliente = registrar_cliente("Teste", "cliente@email.com", "senha123")
        sol = criar_solicitacao(cliente.id, "A", "D")
        respondida = responder_solicitacao(sol.id, "Resposta", "RESOLVIDO")
        assert respondida.status == "RESOLVIDO"
        assert respondida.resposta_atendente == "Resposta"

def test_obter_estatisticas_admin(app):
    with app.app_context():
        cliente = registrar_cliente("T", "t@e.com", "s")
        criar_solicitacao(cliente.id, "A1", "D1")
        sol2 = criar_solicitacao(cliente.id, "A2", "D2")
        responder_solicitacao(sol2.id, "R", "RESOLVIDO")
        
        stats = obter_estatisticas_admin()
        assert stats['abertos'] == 1
        assert stats['resolvidos'] == 1
        assert stats['em_andamento'] == 0
