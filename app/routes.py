from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from app import services
from functools import wraps

routes = Blueprint('main', __name__)

def login_required(perfil=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                return redirect(url_for('main.login'))
            if perfil and session.get('perfil') != perfil:
                flash('Acesso negado: Permissão insuficiente.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = services.autenticar_usuario(request.form['email'], request.form['senha'])
        if usuario:
            session['usuario_id'] = usuario.id
            session['perfil'] = usuario.perfil
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', erro="Credenciais inválidas")
    return render_template('login.html')

@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@routes.route('/cliente/nova-solicitacao', methods=['GET', 'POST'])
@login_required(perfil='CLIENTE')
def nova_solicitacao():
    if request.method == 'POST':
        services.criar_solicitacao(session['usuario_id'], request.form['assunto'], request.form['descricao'])
        flash('Solicitação criada com sucesso!', 'success')
        return redirect(url_for('main.minhas_solicitacoes'))
    return render_template('cliente/nova_solicitacao.html')

@routes.route('/cliente/minhas-solicitacoes')
@login_required(perfil='CLIENTE')
def minhas_solicitacoes():
    solicitacoes = services.listar_solicitacoes_cliente(session['usuario_id'])
    return render_template('cliente/minhas_solicitacoes.html', solicitacoes=solicitacoes)

@routes.route('/atendente/fila')
@login_required(perfil='ATENDENTE')
def fila_atendimento():
    solicitacoes = services.listar_fila_atendimento()
    return render_template('atendente/fila.html', solicitacoes=solicitacoes)

@routes.route('/atendente/responder/<int:id>', methods=['GET', 'POST'])
@login_required(perfil='ATENDENTE')
def responder_solicitacao_route(id):
    if request.method == 'POST':
        services.responder_solicitacao(id, request.form['resposta'], request.form['status'])
        flash(f'Solicitação #{id} respondida.', 'success')
        return redirect(url_for('main.fila_atendimento'))
    
    solicitacao = services.buscar_solicitacao_por_id(id)
    if not solicitacao:
        flash('Solicitação não encontrada.', 'warning')
        return redirect(url_for('main.fila_atendimento'))
    return render_template('atendente/responder.html', solicitacao=solicitacao)

@routes.route('/admin/dashboard', methods=['GET'])
@login_required(perfil='ADMIN')
def admin_dashboard():
    estatisticas = services.obter_estatisticas_admin()
    return render_template('admin/dashboard.html', dados=estatisticas)

@routes.route('/')
def index():
    if 'usuario_id' in session:
        perfil = session.get('perfil')
        if perfil == 'CLIENTE':
            return redirect(url_for('main.minhas_solicitacoes'))
        elif perfil == 'ATENDENTE':
            return redirect(url_for('main.fila_atendimento'))
        elif perfil == 'ADMIN':
            return redirect(url_for('main.admin_dashboard'))
    return redirect(url_for('main.login'))
