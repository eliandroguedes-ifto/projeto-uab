# Especificação do Sistema de Atendimento

Abaixo está a especificação técnica detalhada, estruturada de forma determinística e granular para orientar a implementação do código-fonte do Sistema de Atendimento ao Cliente.

## 1. Infraestrutura e Configuração

### /.env
*   **Ação**: criar
*   **Descrição**: Arquivo de configuração de variáveis de ambiente do sistema. Deve ser ignorado pelo Git.
*   **Pseudocódigo**:
    ```dotenv
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=gerar_chave_aleatoria_segura_aqui
    DATABASE_URI=sqlite:///../instance/database.sqlite
    ADMIN_INITIAL_EMAIL=admin@sistema.com
    ADMIN_INITIAL_PASSWORD=SenhaAdmin123!
    ```

### /requirements.txt
*   **Ação**: criar
*   **Descrição**: Lista de dependências Python estritas para instalação via pip.
*   **Pseudocódigo**:
    ```txt
    Flask==3.0.0
    Flask-SQLAlchemy==3.1.1
    Flask-Bcrypt==1.0.1
    python-dotenv==1.0.0
    gunicorn==21.2.0
    pytest==7.4.3
    pytest-mock==3.12.0
    pytest-cov==4.1.0
    ```

### /.gitignore
*   **Ação**: criar
*   **Descrição**: Define os arquivos e diretórios que o controle de versão Git deve ignorar.
*   **Pseudocódigo**:
    ```gitignore
    .env
    __pycache__/
    *.sqlite
    ```

### /Dockerfile
*   **Ação**: criar
*   **Descrição**: Instruções de construção do contêiner da aplicação web.
*   **Pseudocódigo**:
    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    EXPOSE 5000
    CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
    ```

## 2. Modelos de Dados (Models)

### /app/models.py
*   **Ação**: criar
*   **Descrição**: Define o esquema relacional do banco de dados utilizando Flask-SQLAlchemy.
*   **Pseudocódigo**:
    ```python
    from app import db
    from datetime import datetime

    class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        nome = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(128), unique=True, nullable=False)
        senha_hash = db.Column(db.String(256), nullable=False)
        perfil = db.Column(db.String(10), nullable=False) # Valores permitidos: 'CLIENTE', 'ATENDENTE', 'ADMIN'

    class Solicitacao(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
        assunto = db.Column(db.String(150), nullable=False)
        descricao = db.Column(db.Text, nullable=False)
        status = db.Column(db.String(20), default='ABERTO', nullable=False) # 'ABERTO', 'EM_ANDAMENTO', 'RESOLVIDO'
        resposta_atendente = db.Column(db.Text, nullable=True)
        data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ```

## 3. Lógica de Negócio (Services)

### /app/services.py
*   **Ação**: criar
*   **Descrição**: Módulo que encapsula as regras de negócio de autenticação, usuários e solicitações.
*   **Pseudocódigo**:
    ```python
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
    ```

## 4. Controladores (Routes)

### /app/routes.py
*   **Ação**: criar
*   **Descrição**: Mapeamento de rotas HTTP, extração de parâmetros de requisição e injeção de dados nas views.
*   **Pseudocódigo**:
    ```python
    from flask import Blueprint, request, session, render_template, redirect, url_for
    from app import services

    routes = Blueprint('main', __name__)

    @routes.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            usuario = services.autenticar_usuario(request.form['email'], request.form['senha'])
            if usuario:
                session['usuario_id'] = usuario.id
                session['perfil'] = usuario.perfil
                return redirect(url_for('main.index')) # Assumindo uma rota 'index'
            else:
                return render_template('login.html', erro="Credenciais inválidas")
        return render_template('login.html')

    @routes.route('/cliente/nova-solicitacao', methods=['GET', 'POST'])
    def nova_solicitacao():
        if 'perfil' not in session or session['perfil'] != 'CLIENTE':
            return redirect(url_for('main.login'))
        if request.method == 'POST':
            services.criar_solicitacao(session['usuario_id'], request.form['assunto'], request.form['descricao'])
            return redirect(url_for('main.minhas_solicitacoes')) # Assumindo rota 'minhas_solicitacoes'
        return render_template('cliente/nova_solicitacao.html')

    @routes.route('/atendente/responder/<int:id>', methods=['POST'])
    def responder_solicitacao_route(id):
        if 'perfil' not in session or session['perfil'] != 'ATENDENTE':
            return redirect(url_for('main.login'))
        services.responder_solicitacao(id, request.form['resposta'], request.form['status'])
        return redirect(url_for('main.fila_atendimento')) # Assumindo rota 'fila_atendimento'

    @routes.route('/admin/dashboard', methods=['GET'])
    def admin_dashboard():
        if 'perfil' not in session or session['perfil'] != 'ADMIN':
            return redirect(url_for('main.login'))
        estatisticas = services.obter_estatisticas_admin()
        return render_template('admin/dashboard.html', dados=estatisticas)

    @routes.route('/')
    def index():
        if 'usuario_id' in session:
            if session['perfil'] == 'CLIENTE':
                return redirect(url_for('main.minhas_solicitacoes'))
            elif session['perfil'] == 'ATENDENTE':
                return redirect(url_for('main.fila_atendimento'))
            elif session['perfil'] == 'ADMIN':
                return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.login'))

    # Rotas placeholder para completude
    @routes.route('/cliente/minhas-solicitacoes')
    def minhas_solicitacoes():
        return "Página de Minhas Solicitações (Implementar)"

    @routes.route('/atendente/fila')
    def fila_atendimento():
        return "Página da Fila de Atendimento (Implementar)"
    ```

## 5. Inicialização da Aplicação

### /app/__init__.py
*   **Ação**: criar
*   **Descrição**: Configuração da fábrica de aplicativos do Flask, inicialização do banco de dados e rotina de seed do administrador.
*   **Pseudocódigo**:
    ```python
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
    ```

### /run.py
*   **Ação**: criar
*   **Descrição**: Ponto de entrada para execução da aplicação Flask localmente ou via WSGI.
*   **Pseudocódigo**:
    ```python
    from app import create_app
    import os

    app = create_app()

    if __name__ == '__main__':
        # Define host e port de forma mais robusta
        host = os.getenv('FLASK_HOST', '127.0.0.1')
        port = int(os.getenv('FLASK_PORT', 5000))
        app.run(host=host, port=port, debug=True) # debug=True para desenvolvimento
    ```