# Minha API

**Descrição do Sistema de Gerenciamento de Tarefas e Blocos Padrão**

Visão Geral do Sistema

O sistema é projetado para oferecer uma solução de gerenciamento de tarefas e blocos padrão, ideal para pessoas que buscam otimizar a alocação de seu tempo diário (as 24 horas do dia). O foco principal é permitir que os usuários criem, gerenciem e monitorem tarefas agrupadas em blocos padrão, com aplicação em diversos cenários de atividade da vida das pessoas.

Objetivos de Negócio

    Melhoria da Eficácia Operacional: Automatizar o planejamento de tarefas repetitivas e rotineiras para reduzir o tempo de setup e evitar que a pessoa se perca durante o dia em tarefas não planejadas e dispersantes.
    Flexibilidade na Gestão de Tarefas: Facilitar a customização e ajustes de tarefas e blocos de trabalho conforme necessidades específicas da pessoa.
    Visibilidade Aprimorada: Prover relatórios detalhados e visualizações claras das atividades planejadas e sua execução, ajudando na tomada de decisão e na melhoria contínua das atividades diárias (sem funcionalidades ainda disponíveis nesta primeira versão).

Características Principais

    Gestão de Tarefas e Blocos Padrão: Criação e gerenciamento de tarefas individuais e agrupamento delas em blocos padrão, cada um podendo ser configurado para ocorrer em dias específicos da semana.
	Relatórios com as tarefas mais executadas e a transparência da diferença entre o planejado e executado.

Tecnologias Utilizadas

    Python e Pydantic: O backend é construído em Python, utilizando a biblioteca Pydantic para a validação de dados e definição de esquemas, garantindo que as informações manipuladas estejam corretas e sejam fáceis de integrar com outras plataformas.
    SQLAlchemy: Utilizado para ORM (Object-Relational Mapping), facilitando a manipulação e consulta de dados em bancos de dados SQL, proporcionando escalabilidade e segurança nas operações de dados.
    Flask: Framework leve que oferece liberdade e flexibilidade na criação de APIs web, permitindo uma fácil escalabilidade do sistema e integração com outras ferramentas e sistemas.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

## Banco de Dados

O banco de dados será criado na primeira execução.
Caso deseje realizar uma carga de dados de exemplo, deve-se executar o script python CARGA.PY que está na pasta model.