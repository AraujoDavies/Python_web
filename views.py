# arquivo com todas as rotas do nosso site
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from config import UPLOAD_PATH
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import FormularioUsuario, recupera_imagem, deleta_arquivo, FormularioJogo
import time

# rotas com interface...
@app.route('/') 
def index():
    lista = Jogos.query.order_by(Jogos.id) # pegando itens do banco na ordenado pelo ID
    # Usando render_template pela primeira vez
    return render_template('lista.html', titulo='Jogos', jogos=lista) 

@app.route('/login')
def login():
    if 'usuario_logado' in session:
        if session['usuario_logado'] != None: # se tiver logado já
            flash('Já está logado', 'info')
            return redirect(url_for('index'))
    form = FormularioUsuario()
    proxima = request.args.get('proxima') # outro caso de uso do request... pega o atributo 'proxima' na url
    return render_template('login.html', proxima=proxima, titulo = 'Login',form=form) # passa o atributo para o html

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

# rota com img
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

# rotas do CRUD
@app.route('/novo')
def novo():
    # se a na sessão nao tem a chave 'usuario_logado' ou tem e está com valor None...
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # usando url_for pela primeira vez. login == nome da def
        return redirect(url_for('login', proxima=url_for('novo'))) # Próxima é o value q está no input hidden em login.html
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/editar/<int:id>')
def editar(id):
    # se na sessão nao tem a chave 'usuario_logado' ou tem e está com valor None... (se não logado)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('editar', proxima=url_for('editar')))
        
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' in session and session['usuario_logado'] != None:
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Jogo Deletado com sucesso!')
    else:
        flash('Você não está logado!')
    return redirect(url_for('index'))


################################ rotas com POST ################################

# GET p pegar informações e POST para enviar informações pois tem uma camada de segurança
@app.route('/criar', methods=['POST',]) # methods: servidor só aceita GET, POST tem q ser passado
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('index'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    """ COMO PUXAR DADOS DE UM FORMS USANDO REQUEST
    nome = request.form['nome'] # usando request pela primeira vez, ele busca o atributo name no novo.html
    categoria = request.form['categoria']
    console = request.form['console']
    """
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo'] # pegando uploads de arquivos    
    if arquivo.filename:
        timestamp = time.time() # ajuda para q cada vez crie um arquivo único, para evitar q a img antiga fique em cash e force a request
        arquivo.save(f'{UPLOAD_PATH}/capa{novo_jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST',]) # methods: servidor só aceita GET, POST tem q ser passado
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        
        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time() 
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario and form.senha.data == usuario.senha:
        # if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!') # primeiro exemplo de uso do FLASH
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))