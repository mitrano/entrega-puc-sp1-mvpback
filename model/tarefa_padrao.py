from sqlalchemy import Column, String, Integer, ForeignKey
from model import Base
from sqlalchemy.orm import relationship, backref

class Tarefa_Padrao(Base):
    """
    Modelo SQLAlchemy para a tabela 'tarefa_padrao'.
    Esta classe define a estrutura de uma Tarefa Padrão associada a um Bloco Padrão.

    Atributos:
        id_tarefa_padrao (int): Chave primária, autoincrementada.
        detalhes (str): Detalhes específicos da tarefa.
        tempo (int): Tempo estimado para completar a tarefa em minutos.
        id_tarefa_tipo (int): Chave estrangeira que aponta para o tipo de tarefa correspondente.
        id_bloco_padrao (int): Chave estrangeira que aponta para o bloco padrão ao qual a tarefa pertence.

    Relacionamentos:
        bloco_padrao (relationship): Relaciona esta tarefa ao seu bloco padrão correspondente.
        tarefa_tipo (relationship): Relaciona esta tarefa ao seu tipo de tarefa correspondente.
    """

    __tablename__ = 'tarefa_padrao'  # Nome da tabela no banco de dados

    # Definição das colunas do banco de dados
    id_tarefa_padrao = Column("id_tarefa_padrao", Integer, primary_key=True, autoincrement=True)
    detalhes = Column(String(300))  # Detalhes da tarefa com limite de 300 caracteres
    tempo = Column(Integer)  # Tempo estimado em minutos

    # Chaves estrangeiras para ligar com outras tabelas
    id_tarefa_tipo = Column("id_tarefa_tipo", Integer, ForeignKey("tarefa_tipo.id_tarefa_tipo"), nullable=False)
    id_bloco_padrao = Column("id_bloco_padrao", Integer, ForeignKey("bloco_padrao.id_bloco_padrao"), nullable=False)
    
    # Relacionamentos com outras tabelas, incluindo backrefs para acesso reverso
    bloco_padrao = relationship('Bloco_Padrao', backref=backref('tarefas_padrao_backref', lazy=True))
    tarefa_tipo = relationship('Tarefa_Tipo', backref=backref('tarefa_tipo_backref', lazy=True))

    def __init__(self, id_bloco_padrao: int, id_tarefa_tipo: int, detalhes: str, tempo: int):
        """
        Construtor para a classe Tarefa_Padrao.

        Parâmetros:
            id_bloco_padrao (int): ID do bloco padrão ao qual a tarefa está associada.
            id_tarefa_tipo (int): ID do tipo de tarefa associado à tarefa.
            detalhes (str): Descrição ou detalhes da tarefa.
            tempo (int): Tempo estimado para a conclusão da tarefa em minutos.
        """
        self.detalhes = detalhes
        self.tempo = tempo
        self.id_bloco_padrao = id_bloco_padrao
        self.id_tarefa_tipo = id_tarefa_tipo

    def to_dict(self):
        """
        Converte o objeto Tarefa_Padrao em um dicionário Python, útil para serialização.

        Retorna:
            Um dicionário com as propriedades da Tarefa Padrão.
        """
        return {
            "id_tarefa_padrao": self.id_tarefa_padrao,
            "detalhes": self.detalhes,
            "tempo": self.tempo,
            "id_bloco_padrao": self.id_bloco_padrao,
            "id_tarefa_tipo": self.id_tarefa_tipo,
            "descricao_tarefa_tipo": self.tarefa_tipo.descricao if self.tarefa_tipo else None
        }
