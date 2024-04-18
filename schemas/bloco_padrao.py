from pydantic import BaseModel
from typing import List
from model.bloco_padrao import Bloco_Padrao
import json

class TarefaPadraoSchema(BaseModel):
    """
    Modelo para entrada de dados de uma tarefa padrão.
    """
    detalhes: str  # Descrição detalhada da tarefa.
    tempo: int     # Tempo necessário para completar a tarefa, em minutos.
    id_tarefa_tipo: int  # ID do tipo de tarefa ao qual esta tarefa está associada.

class TarefaPadraoViewSchema(BaseModel):
    """
    Modelo para visualização dos dados de uma tarefa padrão.
    """
    detalhes: str  # Descrição detalhada da tarefa.
    tempo: int     # Tempo necessário para completar a tarefa, em minutos.
    id_tarefa_tipo: int  # ID do tipo de tarefa ao qual esta tarefa está associada.
    id_tarefa_padrao: int  # ID único da tarefa padrão.
    descricao_tarefa_tipo: str  # Descrição textual do tipo de tarefa.

class BlocoPadraoViewSchema(BaseModel):
    """
    Modelo para definir como um bloco padrão é retornado.
    """
    id_bloco_padrao: int  # ID único do bloco padrão.
    descricao: str  # Descrição do bloco padrão.
    tempo: int  # Tempo total estimado para completar todas as tarefas do bloco, em minutos.
    dias_semana: str  # Representação dos dias da semana que o bloco abrange, como uma string.
    tarefas: List[TarefaPadraoViewSchema]  # Lista de tarefas padrão associadas a este bloco.

class BlocoPadraoDeleteSchema(BaseModel):
    """
    Modelo que define os parâmetros para deleção de um bloco padrão.
    """
    id_bloco_padrao: int  # ID do bloco padrão que será deletado.

class BlocoPadraoSchema(BaseModel):
    """ 
    Modelo para entrada de dados de um bloco padrão.
    """
    descricao: str  # Descrição do bloco.
    tempo: int  # Tempo total necessário para completar todas as tarefas do bloco, em minutos.
    dias_semana: str  # Dias da semana em que o bloco é aplicável, representados como uma string.
    tarefas: List[TarefaPadraoSchema]  # Lista de tarefas padrão que compõem este bloco.

    class Config:
        orm_mode = True  # Ativa o modo ORM, permitindo o uso com bancos de dados ORM.
        from_attributes = True  # Permite a criação automática de modelos a partir de atributos ORM.

def apresenta_bloco_padrao(bloco_padrao: Bloco_Padrao):
    """
    Retorna uma representação de um bloco padrão conforme definido em BlocoPadraoViewSchema.
    """
    return {
        "id_bloco_padrao": bloco_padrao.id_bloco_padrao,
        "descricao": bloco_padrao.descricao,
        "tempo": bloco_padrao.tempo,
        "dias_semana": bloco_padrao.dias_semana,
        "tarefas": [tarefa.to_dict() for tarefa in bloco_padrao.tarefas]  # Converte cada tarefa do bloco em dicionário.
    }

class TarefaPadraoCreateSchema(BaseModel):
    """
    Modelo para criação de uma nova tarefa padrão.
    """
    detalhes: str  # Descrição da tarefa.
    tempo: int  # Tempo necessário para completar a tarefa, em minutos.

class BlocoPadraoCreateSchema(BaseModel):
    """
    Modelo para criação de um novo bloco padrão.
    """
    descricao: str = "Dias de Semana"  # Descrição padrão do bloco.
    tempo: int = 1440  # Tempo total padrão, em minutos, para todas as tarefas do bloco.
    dias_semana: str = "0111110"  # Padrão de dias da semana, representados como uma string binária.
    tarefas: List[TarefaPadraoCreateSchema] = []  # Lista inicial vazia de tarefas padrão.
    id_bloco_padrao: int = 1  # ID padrão inicial para um novo bloco.
