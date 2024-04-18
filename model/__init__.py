from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import logging

from sqlalchemy import event
from sqlalchemy.engine import Engine

# importando os elementos definidos no modelo
from model.base import Base

from model.tarefa_tipo import Tarefa_Tipo
from model.bloco_padrao import Bloco_Padrao
from model.tarefa_padrao import Tarefa_Padrao

# Define o nome do arquivo do banco de dados
db_name = "db.sqlite4"

# Define o diretório onde o banco de dados deve ser armazenado
db_path = os.path.join(os.getcwd(), "database")
print(db_path)

# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # Então cria o diretório
    os.makedirs(db_path)

# Constrói a URL de conexão utilizando o caminho absoluto
db_url = f'sqlite:///{os.path.join(db_path, db_name)}'

# Configura o handler e o formato do log
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Configura o logger do SQLAlchemy
logger = logging.getLogger('sqlalchemy.engine')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Configuração do logging para arquivo
logging.basicConfig(filename='sqlalchemy_log.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Configurando o logger do engine do SQLAlchemy para DEBUG
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=True)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
