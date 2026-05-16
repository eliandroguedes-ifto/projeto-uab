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
*   **Ação**: refatorar
*   **Descrição**: Módulo centralizado de lógica de negócio com otimizações de desempenho.
*   **Recursos Otimizados**:
    *   **Cache**: Implementação de `Flask-Caching` (SimpleCache) para estatísticas do dashboard admin (timeout: 300s). Invalidação automática em escritas.
    *   **Jobs/Filas**: Simulação de processamento assíncrono usando `threading.Thread` para notificações de criação e resposta de chamados.
    *   **Modularidade**: Organização das funções por domínio (Auth, Ticket, Admin).

## 4. Controladores (Routes)

### /app/routes.py
*   **Ação**: refatorar
*   **Descrição**: Gerenciamento de rotas com segurança e feedback aprimorados.
*   **Melhorias de Refatoração**:
    *   **Decorator de Autorização**: Uso de `@login_required(perfil=...)` para eliminar duplicidade de verificações de sessão e perfil.
    *   **Feedback ao Usuário**: Implementação de `flash` messages para confirmar ações (criação, resposta, erro).
    *   **Simplicidade**: Delegação total da lógica de busca e persistência para o módulo de Services.

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

## 6. Especificação de Frontend

### 6.1 Design System e Identidade Visual
*   **Paleta de Cores**:
    *   Primária: `#0d6efd` (Blue Bootstrap)
    *   Sucesso: `#198754` (Green)
    *   Aviso: `#ffc107` (Yellow)
    *   Erro/Perigo: `#dc3545` (Red)
    *   Fundo: `#f8f9fa` (Light Gray)
    *   Texto Principal: `#212529`
*   **Tipografia**: Sans-serif (Inter, system-ui).
*   **Componentes**:
    *   **Cards**: Border-radius de 10px, sombra leve (`box-shadow: 0 4px 6px rgba(0,0,0,0.1)`).
    *   **Botões**: Altura mínima de 44px para mobile (área de toque).
    *   **Badges**: Arredondadas para indicação de status.

### 6.2 Responsividade
*   **Mobile (< 768px)**:
    *   Formulários ocupam 100% da largura.
    *   Tabelas com `overflow-x: auto`.
    *   Menu hambúrguer para navegação.
*   **Tablet (768px - 1024px)**:
    *   Grids de 2 colunas para cards de resumo.
*   **Desktop (> 1024px)**:
    *   Layout centralizado com container de 1140px.

### 6.3 Acessibilidade (A11y)
*   **Navegação**: Foco visível em todos os elementos interativos.
*   **ARIA**: Uso de `aria-label` em botões de ícone e `role="alert"` em mensagens de erro.
*   **Contraste**: Garantir proporção mínima de 4.5:1 para textos.
*   **Semântica**: Uso correto de `<main>`, `<nav>`, `<h1>`-`<h6>`.

### 6.4 Estados e Feedbacks
*   **Carregamento**: Uso de spinners Bootstrap em botões durante o submit.
*   **Vazio (Empty States)**: Ilustração ou ícone centralizado com texto instrutivo quando não houver dados.
*   **Erro**: Alertas (`.alert-danger`) fixos no topo do formulário ou toast notifications.
*   **Sucesso**: Redirect com mensagens flash informativas.

### 6.5 Fluxos de Navegação
*   **Breadcrumbs**: Presentes em páginas de detalhe/edição para facilitar o retorno.
*   **Feedback de Ação**: Botões mudam de estado (disabled) após clique para evitar submissões duplas.
    ```