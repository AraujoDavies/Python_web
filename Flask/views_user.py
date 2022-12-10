# arquivo com todas as rotas relacionadas aos USUÁRIOS do nosso site
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    if 'usuario_logado' in session:
        if session['usuario_logado'] != None: # se tiver logado já
            flash('Já está logado')
            return redirect(url_for('index'))
    form = FormularioUsuario()
    proxima = request.args.get('proxima') # outro caso de uso do request... pega o atributo 'proxima' na url
    return render_template('login.html', proxima=proxima, titulo='Login',form=form) # passa o atributo para o html

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


@app.route('/autenticar', methods=['POST',])
def autenticar():
    try:
        form = FormularioUsuario(request.form)
        usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
        senha = check_password_hash(usuario.senha, form.senha.data)
        if usuario and senha:
            # if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!') # primeiro exemplo de uso do FLASH
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))
    except:
        return '<h2> erro </h2>'