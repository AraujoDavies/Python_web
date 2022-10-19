# Arquivo responsável por guardar as Config 

SECRET_KEY = 'hash_de_letras_aleatorias'

# configurando URI de conexão pelo SQLALCHEMY
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector', # bom de usar o ALCHEMY é caso eu migre o DB, não precisa mudar o código
        usuario = 'root', # o ruim é a integração com sistemas legados
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    )

import os

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

# print(UPLOAD_PATH)