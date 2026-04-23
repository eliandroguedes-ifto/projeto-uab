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
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', erro="Credenciais inválidas")
    return render_template('login.html')

@routes.route('/cliente/nova-solicitacao', methods=['GET', 'POST'])
def nova_solicitacao():
    if 'perfil' not in session or session['perfil'] != 'CLIENTE':
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        services.criar_solicitacao(session['usuario_id'], request.form['assunto'], request.form['descricao'])
        return redirect(url_for('main.minhas_solicitacoes'))
    return render_template('cliente/nova_solicitacao.html')

@routes.route('/atendente/responder/<int:id>', methods=['POST'])
def responder_solicitacao_route(id):
    if 'perfil' not in session or session['perfil'] != 'ATENDENTE':
        return redirect(url_for('main.login'))
    services.responder_solicitacao(id, request.form['resposta'], request.form['status'])
    return redirect(url_for('main.fila_atendimento'))

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

@routes.route('/cliente/minhas-solicitacoes')
def minhas_solicitacoes():
    return "Página de Minhas Solicitações (Implementar)"

@routes.route('/atendente/fila')
def fila_atendimento():
    return "Página da Fila de Atendimento (Implementar)"
