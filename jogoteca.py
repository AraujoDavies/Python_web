# Arquivo main do q centraliza tudo

# pip install flask==2.0.2
from flask import Flask
# pip install flask-sqlalchemy==2.5.1 --> ORM q faz a comunicação entre servidor flask e database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app) # instanciando o DB

from views import *        

""" if abaixo para controle de escopo, ou seja, os códigos que foram importados de outro arquivo não
    serão executados. exemplo:
    
    nesse arquivo: __name__ = '__main__'
    import config: config.__name__ = 'config'
    import models: models.__name__ = 'models'
"""
if __name__ == '__main__': # só executa os códigos desse arquivo que é o main. 
    app.run(debug=True) # posso passar tambem o host e a porta como parametro, mas ñ deve ser feito em PROD