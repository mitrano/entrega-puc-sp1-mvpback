# Importa as bibliotecas necessárias para a API, tratamento de erros, e interação com o banco de dados
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, jsonify
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import aliased
from schemas import *  # Importa todas as classes de esquema para validação de dados
from model import Tarefa_Tipo, Session, Bloco_Padrao, Tarefa_Padrao  # Importa os modelos do banco de dados
from logger import logger  # Importa o módulo de log personalizado

from flask_cors import CORS  # Importa o módulo para permitir Cross-Origin Resource Sharing

# Define informações básicas sobre a API utilizando OpenAPI 3
info = Info(title="API Daily Plan", version="1.0.0")
app = OpenAPI(__name__, info=info)  # Cria a aplicação Flask configurada com OpenAPI
CORS(app)  # Aplica configurações CORS à aplicação Flask para permitir acessos de diferentes origens

# Definindo tags que serão utilizadas na documentação da API para organizar as operações
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefa_tipo_tag = Tag(name="Tipo de Tarefa", description="Adição, visualização e remoção de tipos de tarefa à base")
bloco_padrao_tag = Tag(name="Bloco Padrão", description="Adição, visualização e remoção de blocos padrão e suas respectivas tarefas padrão à base")

@app.post('/bloco', tags=[bloco_padrao_tag],
                    responses={"200": BlocoPadraoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_bloco_padrao(form: BlocoPadraoSchema):
    """
    Endpoint POST para adicionar um Bloco Padrão com suas respectivas tarefas padrão.
    Este endpoint recebe dados de um bloco padrão e suas tarefas associadas, os salva no banco de dados
    e retorna uma representação do bloco padrão adicionado.

    Parâmetros:
        - form (BlocoPadraoSchema): Um objeto schema que contém os dados do bloco padrão e tarefas a serem adicionados.

    Retorna:
        - Uma representação JSON do Bloco Padrão adicionado e código de status HTTP 200 em caso de sucesso.
        - Mensagem de erro e código de status HTTP 409 se ocorrer um erro de integridade (por exemplo, duplicata).
        - Mensagem de erro e código de status HTTP 400 para outros tipos de erros.
    """
    # Instancia um novo objeto Bloco_Padrao usando os dados fornecidos no formulário
    bloco_padrao = Bloco_Padrao(        
        descricao   = form.descricao,
        tempo       = form.tempo,
        dias_semana = form.dias_semana
    )

    # Registra no log o processo de adição do bloco padrão
    logger.debug(f"Adicionando bloco padrão de descricao: '{bloco_padrao.descricao}'")
    
    try:
        # Cria uma sessão de conexão com o banco de dados
        session = Session()
        
        # Adiciona o bloco padrão à sessão
        session.add(bloco_padrao)
        session.flush()  # Libera o SQL para o banco sem commit para capturar erros como de integridade

        # Itera sobre cada tarefa incluída no formulário para adicionar ao bloco padrão
        for tarefa in form.tarefas:
            nova_tarefa = Tarefa_Padrao(                
                detalhes=tarefa.detalhes,
                tempo=tarefa.tempo,
                id_tarefa_tipo=tarefa.id_tarefa_tipo,
                id_bloco_padrao=bloco_padrao.id_bloco_padrao  # Vincula a tarefa ao bloco padrão
            )
            session.add(nova_tarefa)
        
        # Comita todas as adições feitas à sessão
        session.commit()
        # Retorna a representação do bloco padrão adicionado e o código de status 200
        return apresenta_bloco_padrao(bloco_padrao), 200

    except IntegrityError as e:  # Captura erros de integridade, como entradas duplicadas
        session.rollback()  # Desfaz todas as mudanças na sessão desde o último commit
        error_msg = "Bloco padrão com a mesma descrição já salvo na base: " + str(e)
        logger.warning(f"Erro ao adicionar bloco padrão '{bloco_padrao.descricao}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:  # Captura qualquer outro tipo de erro não previsto
        session.rollback()
        error_msg = "Não foi possível salvar o novo item: " + str(e)
        logger.warning(f"Erro ao adicionar bloco padrão '{bloco_padrao.descricao}', {error_msg}")
        return {"message": error_msg}, 400

    finally:
        session.close()  # Garante que a sessão é fechada após o tratamento de todos os casos

@app.delete('/apagar_bloco_padrao', tags=[bloco_padrao_tag],
            responses={"200": {"description": "Bloco Padrão deletado com sucesso"},
                       "404": ErrorSchema,
                       "400": ErrorSchema})
def delete_bloco_padrao(query: BlocoPadraoDeleteSchema):
    """
    Endpoint DELETE para deletar um Bloco Padrão e suas respectivas tarefas padrão.
    
    Argumentos:
        - query (BlocoPadraoDeleteSchema): Objeto schema que contém o ID do bloco padrão a ser deletado.
    
    Retorna:
        - Mensagem JSON de sucesso com código de status HTTP 200 se deletado.
        - Mensagem JSON de erro com código de status HTTP 404 se o bloco padrão não for encontrado.
        - Mensagem JSON de erro com código de status HTTP 400 se ocorrer um erro durante a deleção.
    """
    session = Session()  # Inicia uma nova sessão de conexão com o banco de dados
    try:
        # Busca o bloco padrão pelo ID fornecido
        bloco_padrao = session.query(Bloco_Padrao).filter(Bloco_Padrao.id_bloco_padrao == query.id_bloco_padrao).first()
        
        if not bloco_padrao:
            # Se não encontrar o bloco padrão, retorna erro 404
            return jsonify({"message": "Bloco Padrão não encontrado"}), 404

        # Deleta todas as tarefas associadas ao bloco padrão
        session.query(Tarefa_Padrao).filter(Tarefa_Padrao.id_bloco_padrao == query.id_bloco_padrao).delete()
        
        # Deleta o próprio bloco padrão
        session.delete(bloco_padrao)
        
        # Efetiva as alterações feitas na sessão
        session.commit()
        
        return jsonify({"message": "Bloco Padrão deletado com sucesso"}), 200

    except SQLAlchemyError as e:
        # Caso ocorra um erro durante o processo, realiza rollback para reverter as alterações
        session.rollback()
        error_msg = f"Erro ao deletar bloco padrão: {str(e)}"
        logger.error(error_msg)
        return jsonify({"message": error_msg}), 400

    finally:
        # Fecha a sessão após a tentativa de deleção, independentemente do resultado
        session.close()

@app.get('/blocos', tags=[bloco_padrao_tag])
def listar_blocos():
    """
    Endpoint GET para buscar todos os Blocos Padrão com suas respectivas tarefas padrão cadastrados.
    A consulta é otimizada com joins e ordenações para agrupar tarefas dentro de cada bloco.

    Retorna:
        - Uma lista JSON de todos os blocos padrão e suas tarefas, formatada conforme o schema de visualização.
    """
    session = Session()  # Cria uma sessão de conexão com o banco de dados

    # Criação de aliases para as tabelas para facilitar a consulta e garantir joins corretos
    TarefaPadraoAlias = aliased(Tarefa_Padrao)
    TarefaTipoAlias = aliased(Tarefa_Tipo)

    # Configuração da consulta para carregar blocos e suas tarefas, incluindo a descrição de tarefa_tipo
    # A consulta junta as tabelas de blocos, tarefas padrão e tipos de tarefa, ordenando-as pelo ID do bloco e descrição do tipo de tarefa
    blocos = session.query(Bloco_Padrao).\
        join(TarefaPadraoAlias, Bloco_Padrao.tarefas).\
        join(TarefaTipoAlias, TarefaPadraoAlias.tarefa_tipo).\
        order_by(Bloco_Padrao.id_bloco_padrao, TarefaTipoAlias.descricao).\
        all()
    resultado = []

    # Iteração sobre cada bloco padrão para construir a representação conforme o schema definido
    for bloco in blocos:        
        bloco_data = {
            'id_bloco_padrao': bloco.id_bloco_padrao,
            'tempo': bloco.tempo,
            'descricao': bloco.descricao,
            'dias_semana': bloco.dias_semana,
            'tarefas': [tarefa.to_dict() for tarefa in bloco.tarefas]  # Assumindo que existe um método to_dict nas tarefas
        }
        # Valida e serializa os dados do bloco usando o schema de visualização
        bloco_schema = BlocoPadraoViewSchema.model_validate(bloco_data)
        resultado.append(bloco_schema.model_dump())

    session.close()  # Fecha a sessão após a consulta
    return jsonify(resultado)  # Retorna os dados serializados e validados em formato JSON

@app.post('/tarefa_tipo', tags=[tarefa_tipo_tag],
          responses={"200": TarefaTipoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa_tipo(form: TarefaTipoSchema):
    """
    Endpoint POST para adicionar um novo tipo de tarefa na base de dados.
    
    Parâmetros:
        - form (TarefaTipoSchema): Um objeto schema que contém os dados do novo tipo de tarefa.

    Retorna:
        - Uma representação JSON do tipo de tarefa adicionado e código de status HTTP 200 em caso de sucesso.
        - Mensagem de erro e código de status HTTP 409 se ocorrer um erro de integridade (por exemplo, duplicata).
        - Mensagem de erro e código de status HTTP 400 para outros tipos de erros.
    """
    # Cria uma nova instância de Tarefa_Tipo a partir dos dados fornecidos
    tarefa_tipo = Tarefa_Tipo(
        descricao=form.descricao,
        tempo=form.tempo,
        id_tarefa_tipo=None  # O ID é gerado automaticamente pelo banco se não for fornecido
    )

    # Registra no log o processo de adição do tipo de tarefa
    logger.debug(f"Adicionando tipo de tarefa de descricao: '{tarefa_tipo.descricao}'")
    
    try:
        # Cria uma sessão de conexão com o banco de dados
        session = Session()
        
        # Adiciona o novo tipo de tarefa à sessão
        session.add(tarefa_tipo)
        
        # Efetiva as alterações na base de dados
        session.commit()
        logger.debug(f"Adicionado tipo de tarefa de descricao: '{tarefa_tipo.descricao}'")

        # Retorna a representação do tipo de tarefa adicionado e o código de status 200
        return apresenta_tarefa_tipo(tarefa_tipo), 200

    except IntegrityError as e:
        # Trata erros de integridade, como duplicidade de descrição
        session.rollback()  # Desfaz as alterações na sessão
        error_msg = f"Tarefa Tipo de mesma descrição já salvo na base :/{str(e)}"
        logger.warning(f"Erro ao adicionar tarefa tipo '{tarefa_tipo.descricao}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Trata qualquer outro tipo de erro não especificado
        session.rollback()
        error_msg = f"Não foi possível salvar novo item :/{str(e)}"
        logger.warning(f"Erro ao adicionar tarefa tipo '{tarefa_tipo.descricao}', {error_msg}")
        return {"message": error_msg}, 400

    finally:
        # Fecha a sessão independente do resultado
        session.close()

@app.post('/tarefa_tipo_alteracao', tags=[tarefa_tipo_tag],
          responses={"200": TarefaTipoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def alter_tarefa_tipo(form: TarefaTipoViewSchema):
    """
    Endpoint POST para alterar um tipo de tarefa existente na base de dados.
    
    Parâmetros:
        - form (TarefaTipoViewSchema): Um objeto schema que contém os dados atualizados do tipo de tarefa.

    Retorna:
        - Uma representação JSON do tipo de tarefa atualizado e código de status HTTP 200 em caso de sucesso.
        - Mensagem de erro e código de status HTTP 409 se ocorrer um erro de integridade (por exemplo, duplicata).
        - Mensagem de erro e código de status HTTP 400 para outros tipos de erros.

    Este método atualiza um tipo de tarefa existente baseado no ID fornecido.
    """
    # Extrai os dados do formulário e cria um objeto Tarefa_Tipo para manipulação
    tarefa_tipo = Tarefa_Tipo(
        descricao=form.descricao,
        tempo=form.tempo,
        id_tarefa_tipo=form.id_tarefa_tipo
    )
    tarefa_tipo_id = form.id_tarefa_tipo  # ID do tipo de tarefa a ser alterado

    logger.debug(f"Alterando tipo de tarefa de ID: '{tarefa_tipo_id}'")

    try:
        session = Session()  # Cria uma sessão de conexão com o banco de dados
        
        # Atualiza o tipo de tarefa se ele existir
        qtd = session.query(Tarefa_Tipo).filter(Tarefa_Tipo.id_tarefa_tipo == tarefa_tipo_id).update({
            Tarefa_Tipo.descricao: form.descricao,
            Tarefa_Tipo.tempo: form.tempo
        })
        
        session.commit()  # Efetiva as alterações na base de dados
        logger.debug(f"Alterado tipo de tarefa de ID: '{tarefa_tipo_id}'")

        return apresenta_tarefa_tipo(tarefa_tipo), 200  # Retorna a representação atualizada do tipo de tarefa

    except IntegrityError as e:
        # Trata erros de integridade, como duplicidade de descrição
        session.rollback()  # Reverte as alterações na sessão
        error_msg = f"Tarefa Tipo de mesma descrição já salvo na base :/{str(e)}"
        logger.warning(f"Erro ao alterar tarefa tipo '{tarefa_tipo.descricao}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Trata qualquer outro tipo de erro não especificado
        session.rollback()
        error_msg = f"Não foi possível salvar as alterações :/{str(e)}"
        logger.warning(f"Erro ao alterar tarefa tipo '{tarefa_tipo.descricao}', {error_msg}")
        return {"message": error_msg}, 400


@app.delete('/tarefa_tipo_id', tags=[tarefa_tipo_tag],
            responses={"200": TarefaTipoDelIdSchema, "404": ErrorSchema})
def del_produto_id(query: TarefaTipoBuscaIdSchema):
    """
    Endpoint DELETE para deletar um tipo de tarefa específico por ID.
    
    Parâmetros:
        - query (TarefaTipoBuscaIdSchema): Um objeto schema que contém o ID do tipo de tarefa a ser deletado.

    Retorna:
        - Uma mensagem de confirmação com código de status HTTP 200 se o tipo de tarefa foi removido.
        - Uma mensagem de erro com código de status HTTP 404 se o tipo de tarefa não for encontrado ou não puder ser deletado devido a dependências.
    
    A função verifica primeiro se existem tarefas padrão associadas ao tipo de tarefa antes de tentar deletá-lo.
    """
    tarefa_tipo_id = query.id_tarefa_tipo  # Extrai o ID do tipo de tarefa do objeto de consulta
    logger.debug(f"Deletando dados sobre tipo tarefa #{tarefa_tipo_id}")
    
    session = Session()  # Cria uma sessão de conexão com o banco de dados
    
    # Verifica se existem tarefas padrão associadas a esse tipo de tarefa
    count_tarefa_padrao = session.query(Tarefa_Padrao).filter(Tarefa_Padrao.id_tarefa_tipo == tarefa_tipo_id).count()

    if count_tarefa_padrao:
        # Se tarefas padrão estão associadas, não permite a deleção e retorna uma mensagem de erro
        error_msg = f"Existe Tarefa Padrão associada em um Bloco. Não foi possível deletar Tarefa Tipo #{tarefa_tipo_id}"
        logger.debug(error_msg)
        return {"message": error_msg}, 404

    # Realiza a operação de remoção do tipo de tarefa caso não haja dependências
    count = session.query(Tarefa_Tipo).filter(Tarefa_Tipo.id_tarefa_tipo == tarefa_tipo_id).delete()
    session.commit()  # Efetiva as alterações no banco de dados

    if count:
        # Se o tipo de tarefa foi deletado com sucesso, retorna uma mensagem de confirmação
        logger.debug(f"Deletado tipo tarefa #{tarefa_tipo_id}")
        return {"message": "Tipo Tarefa removido", "ID:": tarefa_tipo_id}
    else:
        # Se nenhum tipo de tarefa foi deletado, retorna uma mensagem de erro indicando que não foi encontrado
        error_msg = "Tarefa Tipo não encontrado na base :/"
        logger.warning(f"Erro ao deletar tipo tarefa #'{tarefa_tipo_id}', {error_msg}")
        return {"message": error_msg}, 404

@app.delete('/tarefa_tipo_descricao', tags=[tarefa_tipo_tag],
            responses={"200": TarefaTipoDelSchema, "404": ErrorSchema})
def del_produto(query: TarefaTipoBuscaSchema):
    """
    Endpoint DELETE para deletar um tipo de tarefa específico por descrição.
    
    Parâmetros:
        - query (TarefaTipoBuscaSchema): Um objeto schema que contém a descrição do tipo de tarefa a ser deletado.

    Retorna:
        - Uma mensagem de confirmação com código de status HTTP 200 se o tipo de tarefa foi removido.
        - Uma mensagem de erro com código de status HTTP 404 se o tipo de tarefa não for encontrado.
    
    O método decodifica duas vezes a descrição para garantir que caracteres especiais sejam corretamente interpretados.
    """
    # Decodifica duas vezes a descrição para lidar com possíveis codificações de URL encadeadas
    tarefa_tipo_descricao = unquote(unquote(query.descricao))
    logger.debug(f"Deletando dados sobre tipo tarefa #{tarefa_tipo_descricao}")
    
    session = Session()  # Cria uma sessão de conexão com o banco de dados
    
    # Realiza a operação de remoção do tipo de tarefa correspondente à descrição fornecida
    count = session.query(Tarefa_Tipo).filter(Tarefa_Tipo.descricao == tarefa_tipo_descricao).delete()
    session.commit()  # Efetiva as alterações no banco de dados

    if count:
        # Se o registro foi deletado, retorna uma mensagem de confirmação
        logger.debug(f"Deletado tipo tarefa #{tarefa_tipo_descricao}")
        return {"message": "Tipo Tarefa removido", "Descrição:": tarefa_tipo_descricao}
    else:
        # Se nenhum registro foi deletado, indica que o tipo de tarefa não foi encontrado
        error_msg = "Tarefa Tipo não encontrado na base :/"
        logger.warning(f"Erro ao deletar tipo tarefa #'{tarefa_tipo_descricao}', {error_msg}")
        return {"message": error_msg}, 404


@app.get('/lista_tarefa_tipo', tags=[tarefa_tipo_tag],
         responses={"200": ListagemTarefaTipoSchema, "404": ErrorSchema})
def get_tarefas_tipo():
    """
    Endpoint GET que realiza a busca por todos os Tipos de Tarefa cadastrados na base de dados.
    
    Retorna:
        - Uma representação JSON da listagem de todos os tipos de tarefas, ordenada pela descrição,
          e código de status HTTP 200.
        - Uma resposta vazia com código de status HTTP 200 se não existirem tipos de tarefas cadastrados.
        
    Esta função consulta a base de dados para recuperar todos os tipos de tarefa e organiza a listagem por descrição.
    """
    logger.debug("Listando Tipos de Tarefas")  # Registra no log o início da operação de listagem
    session = Session()  # Cria uma sessão de conexão com o banco de dados
    
    # Realiza a consulta dos tipos de tarefa, ordenando-os pela descrição
    tarefatipos = session.query(Tarefa_Tipo).order_by(Tarefa_Tipo.descricao).all()

    if not tarefatipos:
        # Se não há tipos de tarefa cadastrados, retorna uma lista vazia com status 200
        logger.debug("Nenhum tipo de tarefa encontrado")
        return {"tarefa tipos": []}, 200
    else:
        # Se tipos de tarefa foram encontrados, registra no log a quantidade e retorna os dados
        logger.debug(f"{len(tarefatipos)} tipos de tarefa encontrados")
        return apresenta_tarefa_tipos(tarefatipos), 200

@app.get('/', tags=[home_tag])
def home():
    """
    Endpoint GET para a raiz da API. Redireciona automaticamente para /openapi.
    Este endpoint serve como um conveniente redirecionamento para a tela de escolha
    do estilo de documentação da API, facilitando o acesso direto às opções de documentação disponíveis.

    Retorna:
        - Redirecionamento para a URL /openapi, onde os usuários podem escolher entre diferentes estilos
          de documentação da API, como Swagger, Redoc ou RapiDoc.
    """
    # Redireciona o usuário para a página de documentação da API em /openapi
    return redirect('openapi')

if __name__ == '__main__':
    app.run(debug=True)
