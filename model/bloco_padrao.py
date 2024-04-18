from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from model import Base

class Bloco_Padrao(Base):
    """
    Modelo SQLAlchemy para a tabela 'bloco_padrao'.
    Esta classe define a estrutura do Bloco Padrão que inclui suas tarefas associadas.

    Atributos:
        id_bloco_padrao (int): Chave primária, autoincrementada.
        descricao (str): Descrição do bloco padrão, única para cada bloco.
        tempo (int): Tempo estimado para completar todas as tarefas no bloco, em minutos.
        dias_semana (str): Dias da semana em que o bloco é aplicável, codificados como uma string de 7 caracteres onde cada posição 
            da string representa um dia da semana sendo o primeiro caracter representando o domigo
            e o caracter 7 o sábado. Por exemplo, Blocos para Domingo e sábados seria 
            armazenado assim: 1000001
            0 - Não
            1 - Sim
        tarefas (relationship): Relacionamento com a tabela 'Tarefa_Padrao' que contém todas as tarefas pertencentes a este bloco.
    """

    __tablename__ = 'bloco_padrao'  # Nome da tabela no banco de dados

    # Definição das colunas do banco de dados
    id_bloco_padrao = Column("id_bloco_padrao", Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(140), unique=True)  # Descrição única com limite de 140 caracteres
    tempo = Column(Integer)  # Tempo total em minutos
    dias_semana = Column(String(7))  # String contendo 7 caracteres representando os dias da semana

    # Relacionamento com a tabela de tarefas padrão
    tarefas = relationship("Tarefa_Padrao", back_populates="bloco_padrao")

    def __init__(self, descricao: str, tempo: int, dias_semana: str):
        """
        Construtor para a classe Bloco_Padrao.
        
        Parâmetros:
            descricao (str): Descrição do bloco padrão.
            tempo (int): Tempo total estimado em minutos para completar as tarefas do bloco.
            dias_semana (str): Representação de 7 caracteres dos dias da semana que o bloco se aplica.
        """
        self.descricao = descricao
        self.tempo = tempo                
        self.dias_semana = dias_semana
