# Arquivo como modelos de classes para criação no DATABASE

from jogoteca import db

# criando classes modelo para DB
class Jogos(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

# Como era antes do Banco de dados:
"""
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
"""
