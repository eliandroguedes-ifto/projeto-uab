import pytest
from app import create_app, db
from app.models import Usuario, Solicitacao

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page_accessibility(client):
    """Verifica se a página de login tem elementos de acessibilidade básicos."""
    response = client.get('/login')
    html = response.data.decode('utf-8')
    assert 'role="navigation"' in html
    assert 'aria-label="Formulário de Login"' in html
    assert 'aria-describedby="email-icon"' in html
    assert 'aria-describedby="password-icon"' in html
    assert '<main id="main-content"' in html

def test_empty_states_cliente(client, app):
    """Verifica se o estado vazio é exibido quando não há solicitações."""
    with app.app_context():
        # Criar um usuário cliente
        user = Usuario(nome="Cliente Teste", email="cliente@teste.com", senha_hash="...", perfil="CLIENTE")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with client.session_transaction() as sess:
        sess['usuario_id'] = user_id
        sess['perfil'] = 'CLIENTE'

    response = client.get('/cliente/minhas-solicitacoes')
    html = response.data.decode('utf-8')
    assert 'Nenhuma solicitação encontrada' in html
    assert 'fas fa-clipboard-list' in html # Ícone do estado vazio

def test_loading_state_script(client):
    """Verifica se o script de loading state está presente no base.html."""
    response = client.get('/login')
    html = response.data.decode('utf-8')
    assert 'submitBtn.classList.add(\'btn-loading\')' in html
    assert 'spinner-border' in html

def test_responsive_meta_tag(client):
    """Verifica se a meta tag de viewport está presente."""
    response = client.get('/login')
    html = response.data.decode('utf-8')
    assert 'name="viewport"' in html
    assert 'content="width=device-width, initial-scale=1.0"' in html
