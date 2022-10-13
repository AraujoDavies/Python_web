# pip install flask==2.0.2 | Ideal usar uma versão estável do Flask para nao ter problemas em projetos futuros
from flask import Flask, render_template, request 

class Jogo():
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Fifa', 'Esporte', 'PC, PS e Xbox')
jogo2 = Jogo('Valorant', 'FPS', 'PC')
jogo3 = Jogo('HV Back to Nature', 'Simulator', 'PS1')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__) # instanciando o Flask

@app.route('/hello-world')
def ola_mundo():
    return '<h1>Hello World</h1>'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos: ', jogos=lista) # primeiro uso do render_template

@app.route('/novo-jogo')
def novo():
    return render_template('novo.html', titulo='Cadastrar novo jogo')

@app.route('/criar', methods=['POST',]) # usamos o methods pois o servidor só aceita GET, então temos q avisá-lo
def criar():
    nome = request.form['nome'] # primeiro uso do request
    categoria = request.form['categoria'] # pegamos o atributo 'nome' no HTML
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return render_template('lista.html', titulo='Jogos: ', jogos=lista)

app.run(debug=True) # debug evita reiniciar o servidor para alterações fazerem efeito

# app.run(host='0.0.0.0', port=8080)
"""     
    Observação: não utilizar estas definições para produção, 
    estas opções foram preparadas para ajudar no ambiente de 
    desenvolvimento.
"""