from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo: 
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3] # criando lista de jogos

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Administrator", "admin", "admin")
usuario2 = Usuario("Davies Araujo", "davies", "davies")
usuario3 = Usuario("User qualquer", "other_user", "other_user")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 } # criando dict com usuários para login

app = Flask(__name__)
app.secret_key = 'hash_de_letras_aleatorias'

# Criando primeira rota
@app.route('/') 
def index():
    # Usando render_template pela primeira vez
    return render_template('lista.html', titulo='Jogos', jogos=lista) 

@app.route('/novo')
def novo():
    # se a na sessão nao tem a chave 'usuario_logado' ou tem e está com valor None...
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # usando url_for pela primeira vez. login == nome da def
        return redirect(url_for('login', proxima=url_for('novo'))) # Próxima é o value q está no input hidden em login.html
    return render_template('novo.html', titulo='Novo Jogo')

# GET p pegar informações e POST para enviar informações pois tem uma camada de segurança
@app.route('/criar', methods=['POST',]) # methods: servidor só aceita GET, POST tem q ser passado
def criar():
    nome = request.form['nome'] # usando request pela primeira vez, ele busca o atributo name no novo.html
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima') # outro caso de uso do request... pega o atributo 'proxima' na url
    return render_template('login.html', proxima=proxima, titulo = 'Login') # passa o atributo para o html

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!') # primeiro exemplo de uso do flash
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True) # posso passar tambem o host e a porta como parametro, mas ñ deve ser feito em PROD