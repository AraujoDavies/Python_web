# arquivo com todas as rotas do nosso site

from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos, Usuarios

# Criando primeira rota
@app.route('/') 
def index():
    lista = Jogos.query.order_by(Jogos.id) # pegando itens do banco na ordenado pelo ID
    # Usando render_template pela primeira vez
    return render_template('lista.html', titulo='Jogos', jogos=lista) 

@app.route('/novo')
def novo():
    # se a na sessão nao tem a chave 'usuario_logado' ou tem e está com valor None...
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # usando url_for pela primeira vez. login == nome da def
        return redirect(url_for('login', proxima=url_for('novo'))) # Próxima é o value q está no input hidden em login.html
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/editar/<int:id>')
def editar(id):
    # se a na sessão nao tem a chave 'usuario_logado' ou tem e está com valor None... (se não logado)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:    
        return redirect(url_for('editar', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo)

@app.route('/login')
def login():
    if 'usuario_logado' in session:
        if session['usuario_logado'] != None: # se tiver logado já
            flash('Já está logado')
            return redirect(url_for('index'))
    proxima = request.args.get('proxima') # outro caso de uso do request... pega o atributo 'proxima' na url
    return render_template('login.html', proxima=proxima, titulo = 'Login') # passa o atributo para o html

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo Deletado com sucesso!')
    return redirect(url_for('index'))


################################ rotas com POST ################################

# GET p pegar informações e POST para enviar informações pois tem uma camada de segurança
@app.route('/criar', methods=['POST',]) # methods: servidor só aceita GET, POST tem q ser passado
def criar():
    nome = request.form['nome'] # usando request pela primeira vez, ele busca o atributo name no novo.html
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST',]) # methods: servidor só aceita GET, POST tem q ser passado
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    
    db.session.add(jogo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario and request.form['senha'] == usuario.senha:
        # if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!') # primeiro exemplo de uso do FLASH
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))