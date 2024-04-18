from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from model import Base

class Tarefa_Tipo(Base):
    """
    Modelo SQLAlchemy para a tabela 'tarefa_tipo'.
    Esta classe define a estrutura de um Tipo de Tarefa, que categoriza tarefas padrão.

    Atributos:
        id_tarefa_tipo (int): Chave primária.
        descricao (str): Descrição do tipo de tarefa, deve ser única.
        tempo (int): Tempo padrão estimado para completar uma tarefa deste tipo, expresso em minutos.
        tarefas_padrao (relationship): Relacionamento com a tabela 'Tarefa_Padrao', representando todas as tarefas deste tipo.

    Métodos:
        __init__: Construtor da classe.
    """

    __tablename__ = 'tarefa_tipo'  # Nome da tabela no banco de dados

    # Definição das colunas do banco de dados
    id_tarefa_tipo = Column("id_tarefa_tipo", Integer, primary_key=True)
    descricao = Column(String(140), unique=True)  # Descrição do tipo de tarefa com limite de 140 caracteres, única
    tempo = Column(Integer)  # Tempo estimado em minutos para a execução de tarefas deste tipo

    # Relacionamento com a tabela Tarefa_Padrao
    tarefas_padrao = relationship("Tarefa_Padrao", back_populates="tarefa_tipo")

    def __init__(self, descricao: str, tempo: int, id_tarefa_tipo: int = None):
        """
        Construtor para a classe Tarefa_Tipo.

        Parâmetros:
            descricao (str): Descrição do tipo de tarefa.
            tempo (int): Tempo estimado em minutos para a conclusão de uma tarefa deste tipo.
            id_tarefa_tipo (int, opcional): ID do tipo de tarefa. Se não fornecido, será gerado automaticamente pelo banco de dados se for definido como autoincrement.
        """
        self.descricao = descricao
        self.tempo = tempo
        self.id_tarefa_tipo = id_tarefa_tipo

    def __repr__(self):
        """
        Representação em string da instância da classe, útil para depuração e log.

        Retorna:
            String representando o Tipo de Tarefa.
        """
        return f"<Tarefa_Tipo(id={self.id_tarefa_tipo}, descricao={self.descricao}, tempo={self.tempo})>"
