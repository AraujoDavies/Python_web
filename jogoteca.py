# Arquivo main do q centraliza tudo

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app) # instanciando o DB
csrf = CSRFProtect(app) # o WTForms exige pois faz validação com tokens em ambos lados
bcrypt = Bcrypt(app) # pega os hashs das senhas do database

from views_game import *
from views_user import *

""" if abaixo para controle de escopo, ou seja, os códigos que foram importados de outro arquivo não
    serão executados. exemplo:
    
    nesse arquivo: __name__ = '__main__'
    import config: config.__name__ = 'config'
    import models: models.__name__ = 'models'
"""
if __name__ == '__main__': # só executa os códigos desse arquivo que é o main. 
    app.run(debug=True) # posso passar tambem o host e a porta como parametro, mas ñ deve ser feito em PROD