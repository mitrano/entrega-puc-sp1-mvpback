# API Daily Plan

## Descrição do Sistema de Gerenciamento de Tarefas e Blocos Padrão

### Visão Geral do Sistema

O sistema é projetado para oferecer uma solução de gerenciamento de tarefas e blocos padrão, ideal para pessoas que buscam otimizar a alocação de seu tempo diário (as 24 horas do dia). O foco principal é permitir que os usuários criem, gerenciem e monitorem tarefas agrupadas em blocos padrão, com aplicação em diversos cenários de atividade da vida das pessoas.

### Objetivos de Negócio

- Melhoria da Eficácia Operacional: Automatizar o planejamento de tarefas repetitivas e rotineiras para reduzir o tempo de setup e evitar que a pessoa se perca durante o dia em tarefas não planejadas e dispersantes.
- Flexibilidade na Gestão de Tarefas: Facilitar a customização e ajustes de tarefas e blocos de trabalho conforme necessidades específicas da pessoa.
- Visibilidade Aprimorada: Prover relatórios detalhados e visualizações claras das atividades planejadas e sua execução, ajudando na tomada de decisão e na melhoria contínua das atividades diárias (sem funcionalidades ainda disponíveis nesta primeira versão).

### Características Principais

- Gestão de Tarefas e Blocos Padrão: Criação e gerenciamento de tarefas individuais e agrupamento delas em blocos padrão, cada um podendo ser configurado para ocorrer em dias específicos da semana.
- Relatórios com as tarefas mais executadas e a transparência da diferença entre o planejado e executado.

### Tecnologias Utilizadas

- Python e Pydantic: O backend é construído em Python, utilizando a biblioteca Pydantic para a validação de dados e definição de esquemas, garantindo que as informações manipuladas estejam corretas e sejam fáceis de integrar com outras plataformas.
- SQLAlchemy: Utilizado para ORM (Object-Relational Mapping), facilitando a manipulação e consulta de dados em bancos de dados SQL, proporcionando escalabilidade e segurança nas operações de dados.
- Flask: Framework leve que oferece liberdade e flexibilidade na criação de APIs web, permitindo uma fácil escalabilidade do sistema e integração com outras ferramentas e sistemas.

---
## Como executar 

Para garantir a correta execução deste projeto, é essencial a instalação de todas as bibliotecas Python especificadas no arquivo `requirements.txt`. Após realizar o clone do repositório, por favor, acesse o diretório principal através do terminal para proceder com as seguintes configurações:

### Configuração do Ambiente Virtual

Primeiramente, é necessário criar um ambiente virtual para o projeto, o que pode ser feito através do comando:

```comando
python -m venv ambvir
```

### Instalação das Dependências

Após a ativação do ambiente virtual, instale os pacotes necessários que estão listados no `requirements.txt` usando o comando:

```
(ambvir)$ pip install -r requirements.txt
```

Este comando assegura que todas as dependências necessárias para a execução do projeto sejam instaladas conforme definido no arquivo mencionado.

### Execução da API

Para iniciar a API, execute o seguinte comando:

```
(ambvir)$ flask run --host 0.0.0.0 --port 5000 --reload
```

### Gerenciamento do Banco de Dados

O banco de dados SQLITE será automaticamente criado durante a primeira execução da aplicação. Caso haja a necessidade de carregar dados de exemplo, execute o script `CARGA.PY` encontrado na pasta model. Isso populacionará o banco de dados com informações iniciais necessárias para o uso da aplicação.

O sistema utiliza três tabelas:

- TAREFA_TIPO
  - Tabela mãe de TAREFA_PADRAO (1:N)  - 
- BLOCO_PADRAO
  - Tabela mãe de TAREFA_PADRAO (1:N)
- TAREFA_PADRAO
  - Tabela filha de BLOCO_PADRAO (N:1) - Uma tarefa padrão pode ser inserida várias vezes para um mesmo bloco)
  - Tabela filha de TAREFA_TIPO (N:1) - Uma tarefa padrão podeser inserida várias vezes para uma mesma tarefa_tipo)


---
## Endpoints eleitos para avaliação da disciplina Full Stack Básico - Sprint 01

Estes três endpoints são utilizados na aplicação chamados através do frontend.

### GET /blocos

Endpoint GET para buscar todos os Blocos Padrão com suas respectivas tarefas padrão cadastrados.

### POST /tarefa_tipo

Endpoint POST para adicionar um novo tipo de tarefa na base de dados.

### DELETE /tarefa_tipo_id

Endpoint DELETE para deletar um tipo de tarefa específico por ID.

## Demais Endpoints Utilizados na Aplicação 

Estes endpoints abaixo são utilizados na aplicação (chamados através do frontend).

- POST /tarefa_tipo_alteracao
- GET /listar_tipo_tarefa
- DELETE /apagar_bloco_padrao

## Demais Endpoints não utilizados na aplicação

Estes endpoints abaixo não são utilizados na aplicação, foram criados durante o desenvolvimento mas não houve tempo de incluir a sua chamada pelo front end.

- POST /bloco
- DELETE /tarefa_tipo_descricao
