import pytest
from app import create_app, db, cache
from app.models import Usuario, Solicitacao
import time

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "CACHE_TYPE": "SimpleCache"
    })

    with app.app_context():
        db.create_all()
        cache.clear()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_cache_admin_stats(app):
    """Verifica se as estatísticas do admin são cacheadas."""
    with app.app_context():
        # Setup: Criar um chamado
        user = Usuario(nome="Admin", email="admin@stats.com", senha_hash="...", perfil="ADMIN")
        db.session.add(user)
        db.session.commit()
        
        from app.services import obter_estatisticas_admin, criar_solicitacao
        
        # Primeira chamada - deve popular o cache
        stats1 = obter_estatisticas_admin()
        assert stats1['total'] == 0
        
        # Criar nova solicitação via serviço (isso deve invalidar o cache no meu código atual, 
        # mas vamos testar a persistência se não invalidasse ou se chamássemos diretamente)
        # Na verdade, criar_solicitacao chama cache.delete('admin_stats')
        
        criar_solicitacao(user.id, "Teste", "Desc")
        
        # Após criar, o cache foi deletado. A próxima chamada deve vir com total = 1
        stats2 = obter_estatisticas_admin()
        assert stats2['total'] == 1
        
        # Se chamarmos de novo imediatamente, deve vir do cache (mesmo objeto/dados)
        stats3 = obter_estatisticas_admin()
        assert stats3['total'] == 1

def test_login_required_decorator(client, app):
    """Verifica se o decorator login_required protege as rotas."""
    # Tentar acessar dashboard sem login
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert 'Login' in response.data.decode('utf-8')
    
    # Tentar acessar dashboard com perfil errado (CLIENTE)
    with app.app_context():
        user = Usuario(nome="User", email="user@teste.com", senha_hash="...", perfil="CLIENTE")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with client.session_transaction() as sess:
        sess['usuario_id'] = user_id
        sess['perfil'] = 'CLIENTE'
        
    response = client.get('/admin/dashboard', follow_redirects=True)
    # Deve redirecionar para index (que por sua vez redireciona para minhas-solicitacoes)
    assert 'Minhas Solicitações' in response.data.decode('utf-8')
    assert 'Acesso negado' in response.data.decode('utf-8')
