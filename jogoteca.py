# pip install flask==2.0.2
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello-world')
def home():
    return '<h1>Hello World</h1>'

@app.route('/')
def ola():
    return render_template('lista.html', titulo='Jogos: ')

app.run()

# app.run(host='0.0.0.0', port=8080)
"""     
    Observação: não utilizar estas definições para produção, 
    estas opções foram preparadas para ajudar no ambiente de 
    desenvolvimento.
"""