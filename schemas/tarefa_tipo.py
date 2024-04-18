from pydantic import BaseModel
from typing import Optional, List
from model.tarefa_tipo import Tarefa_Tipo

# from schemas import ComentarioSchema


class TarefaTipoViewSchema(BaseModel):
    """ Define como um tipo de tarefa será retornado.
    """
    id_tarefa_tipo: int = 2
    descricao: str = "Leitura Técnica"
    tempo: Optional[int] = 60

class TarefaTipoSchema(BaseModel):
    """ Define como um novo Tipo de Tarefa a ser inserido deve ser representado
    """
    descricao: str = "Leitura Técnica 2"
    tempo: Optional[int] = 600

def apresenta_tarefa_tipos(tarefa_tipos: List[Tarefa_Tipo]):
    """ Retorna uma representação do tipo de tarefa seguindo o schema definido em
        TipoTarefaViewSchema.
    """
    result = []
    for tarefa_tipo in tarefa_tipos:
        result.append({
            "id_tarefa_tipo": tarefa_tipo.id_tarefa_tipo,
            "descricao": tarefa_tipo.descricao,
            "tempo": tarefa_tipo.tempo
        })

    return {"tarefa_tipos": result}

def apresenta_tarefa_tipo(tarefa_tipo: Tarefa_Tipo):
    """ Retorna uma representação do tipo de tarefa seguindo o schema definido em
        TipoTarefaViewSchema.
    """
    return {
        "id_tarefa_tipo": tarefa_tipo.id_tarefa_tipo,
        "descricao": tarefa_tipo.descricao,
        "tempo": tarefa_tipo.tempo
    }


class TarefaTipoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do tipo de tarefa.
    """
    descricao: str = "Teste"

class TarefaTipoBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do tipo de tarefa.
    """
    id_tarefa_tipo: int = 99


class TarefaTipoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do tipo de tarefa retornado após uma requisição
        de remoção.
    """
    message: str
    descricao: str    

class TarefaTipoDelIdSchema(BaseModel):
    """ Define como deve ser a estrutura do tipo de tarefa retornado após uma requisição
        de remoção.
    """
    message: str
    id_tarefa_tipo: int


class ListagemTarefaTipoSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    tarefa_tipos:List[TarefaTipoSchema]
