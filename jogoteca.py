# pip install flask==2.0.2
from flask import Flask, render_template

class Jogo():
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

app = Flask(__name__)

@app.route('/hello-world')
def home():
    return '<h1>Hello World</h1>'

@app.route('/')
def ola():
    jogo1 = Jogo('Fifa', 'Esporte', 'PC, PS e Xbox')
    jogo2 = Jogo('Valorant', 'FPS', 'PC')
    jogo3 = Jogo('HV Back to Nature', 'Simulator', 'PS1')
    lista = [jogo1, jogo2, jogo3]
    return render_template('lista.html', titulo='Jogos: ', jogos=lista)

app.run()

# app.run(host='0.0.0.0', port=8080)
"""     
    Observação: não utilizar estas definições para produção, 
    estas opções foram preparadas para ajudar no ambiente de 
    desenvolvimento.
"""