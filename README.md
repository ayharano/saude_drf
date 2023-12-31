# **saude-drf** Desafio Lacrei Saúde Back end

Repositório de [Alexandre Harano](mailto:email@ayharano.dev)


## Descrição de Escolhas

Ao longo do desenvolvimento inicial deste projeto, foi escolhido como base o uso de inglês para a parte estrutural, incluindo durante as mensagens de commit no estilo [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) e a parte interna do projeto.

Para a parte mais externa ao projeto, como a exposição de serializadores de dados e endpoints, bem como o README deste projeto, foi utilizado o português junto com mapeamento quando necessário.

A solução foi desenvolvida utilizando um projeto Django chamado `saude_drf` e um app Django chamado `api`.

Junto com a aplicação Django/DRF, foi providenciado a integração com container PostgreSQL através do uso de Docker Compose.
Dessa forma, quem for rodar a aplicação não precisaria configurar manualmente um ambiente virtual Python local.
A configuração utiliza o mapeamento de volumes com o diretório da aplicação junto com a instalação como um pacote editável.
Dessa forma é possível alterar o código e o container da aplicação efetuaria hot reload de mudanças.

A cada parte desenvolvida foram incluídos testes usando o `TestCase` do próprio Django e
o `APITestCase` do DRF para o teste de `ViewSet`s.

### Modelos e Serializadores

Como base de modelos, foram feitas algumas escolhas:

- Todo modelo possui quatro campos:
  - `id`
  - `uuid`
  - `created`
  - `modified`

O raciocínio por trás desses campos é o uso de índice do banco de dados na chave primária autoincremental (`id`),
enquanto que para a exposição externa do dado, seria utilizado UUIDv4 para evitar problemas de enumeração de recursos.

Já os campos `created` e `modified` são utilizados para rastreio de criação e atualização de recursos para uso interno.

Durante esse projeto, foram utilizados dois modelos e respectivos serializadores.

Segue um mapeamento de cada:

#### Profissionais (da Saúde) - Health Care Workers

| Model            | Serializer               |
|------------------|--------------------------|
| `id`             | -                        |
| `uuid`           | `uuid` (somente leitura) |
| `created`        | -                        |
| `modified`       | -                        |
| `legal_name`     | `nome_legal`             |
| `preferred_name` | `nome_social`            |
| `pronouns`       | `pronomes`               |
| `date_of_birth`  | `data_de_nascimento`     |
| `specialization` | `especializacao`         |

Em termos de validação, `nome_social` é o único campo que é aceitável passar vazio (blank).
Outros campos e validações mais específicos para o contexto de profissional de saúde poderiam ser incluídos,
mas não foram adotados.

#### Consultas - Appointments

| Model                | Serializer               |
|----------------------|--------------------------|
| `id`                 | -                        |
| `uuid`               | `uuid` (somente leitura) |
| `created`            | -                        |
| `modified`           | -                        |
| `health_care_worker` | `profissional_uuid`      |
| `preferred_name`     | `nome_social`            |
| `date`               | `data`                   |
| `info`               | `info`                   |

Como comentado anteriormente, para a identificação de recursos foi utilizado UUID.
Dessa forma, o campo `profissional_uuid` foi utilizado uma variação de `SlugRelatedField` do DRF
de maneira que é mapeado para o campo `health_care_worker.uuid` para as interações externas.
Entretanto a nível de modelo, a amarração de `ForeignKey` ainda ocorre usando `health_care_worker.id`.

Em relação a ordenação padrão desse modelo, foi escolhida a ordem crescente de `Appointment.date`.

Quanto às verificações, foram estabelecidas duas restrições, aplicadas a nível de banco de dados com o uso de
[`Constraints`](https://docs.djangoproject.com/en/4.2/ref/models/constraints/)
assim como a nível de serializador:

1. A combinação de profissional e data deve ser única na tabela `Appointment`
2. `Appointment.date` só pode ser posterior ao dia da inserção ou modificação do recurso da consulta

### URLs, Routers e ViewSets

Para o app `api` foi utilizado um `DefaultRouter` do DRF com o namespace de `api`.

Como um passo além do escopo inicial, foi incluída na raiz da URL da aplicação uma visualização de
documentação de OpenAPI.

![Captura de Tela da Página Interativa do OpenAPI](openapi.png "OpenAPI interativo")

Dado que as validações foram tratadas nos modelos e serializadores, o uso de `ModelViewSet`s
para os endpoints de criação, listagem, alteração parcial, alteração total e deleção foram
triviais. Em relação ao desenvolvimento dos endpoint, o que tomou mais tempo foi a inclusão de
testes cobrindo todos as ações de CRUD junto com os casos de erro seja de ausência de dado ou
de alguma validação.

Para a listagem de consultas cadastradas a um profissional em particular, foi utilizado um pacote de
terceiros robusto para que o filtro de `profissional_uuid` pudesse ser aplicado na listagem de consultas.

## Instalação

Clone este repositório e, após [a instalação de Docker Compose](https://docs.docker.com/compose/install/),
utilizando um terminal, vá para a raiz deste projeto e rode

```shell
$ docker compose web up
```

para rodar o projeto Django com o banco de dados PostgreSQL.

O container da aplicação possui um usuário não-root na distribuição Debian e é usado um ambiente virtual de Python 3.11. Desta forma, não é necessária a instalação de um ambiente virtual local.

Demonstrativo de clonando o repositório até subir o container da aplicação:

[![Aplicação rodando](https://asciinema.org/a/skGiq1H6rrSM1mjQEaC6SqriE.png)](https://asciinema.org/a/skGiq1H6rrSM1mjQEaC6SqriE)

### Instalação em ambiente virtual local

Como mencionado anteriormente, não há a necessidade da instalação de ambiente virtual local. Mas caso essa forma seja preferida, recomendamos o uso de pyenv para gerir múltiplas versões de interpretadores Python.

- pyenv (Linux, macOS): [link](https://github.com/pyenv/pyenv)
- pyenv for Windows (Windows): [link](https://pyenv-win.github.io/pyenv-win/)

Uma vez instalado o pyenv, para o desenvolvimento inicial desse projeto foi utilizado o interpretador CPython na versão 3.11.7. Comandos:

```shell
$ pyenv install 3.11.7  # instala a versão CPython 3.11.7
$ pyenv local 3.11.7    # seleciona a versão CPython 3.11.7 como interpretador python local
```

Para o nome do diretório do ambiente virtual, para esse tutorial usaremos `ambientevirtual`.
Caso queira usar outro nome, basta substituir todas as ocorrências a partir daqui.

Para a instalação do ambiente virtual, use os seguintes comandos:

```shell
$ python -m venv ambientevirtual
```

Dessa forma será criado um diretório de nome `ambientevirtual` na raiz do projeto para armazenamento das dependências Python.

### Uso do ambiente virtual local

Em relação à instalação e uso do ambiente virtual em si, maiores informações estão na seguinte página: [documentação do módulo `venv`](https://docs.python.org/3/library/venv.html)

Para o uso do ambiente virtual, segue as instruções de acordo com o sistema operacional:

- venv para Linux ou macOS

```shell
$ source ambientevirtual/bin/activate
```

- venv para Windows (PowerShell)

```powershell
ambientevirtual\Scripts\Activate.ps1
```

#### Instalação das dependências dentro do ambiente virtual

Uma vez que o ambiente virtual esteja ativado, rode o seguinte comando:

```shell
python -m pip install --upgrade pip && python -m pip install --editable '.[test]' && python -m pip install --upgrade tzdata
```

Esse comando é uma cadeia de 3 chamadas consistindo em
1. atualização de `pip` para sua versão mais recente
2. instalação de todas as dependências do projeto, incluindo as de testes, e a definição do projeto atual como [uma dependência editável](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), e
3. garante a instalação do pacote `tzdata`, que é usada pelo Python para gerir informações de timezone sem depender do sistema operacional, em sua última versão estável (explicação na [documentação do módulo `zoneinfo`](https://docs.python.org/3/library/zoneinfo.html))

Após a instalação das dependências, para qualquer interação com o projeto Django, é necessário que o terminal esteja no diretório `src` visto que o arquivo `manage.py` encontra-se lá.

## Execução dos testes

Uma vez que o projeto esteja devidamente instalado, use o seguinte comando para executar a suite de testes da aplicação:

```shell
$ docker compose run web python manage.py test
```

Demonstrativo de rodando os testes da aplicação:

[![Testes](https://asciinema.org/a/EFZH6EAx563iSWSCiaavDHtP2.png)](https://asciinema.org/a/EFZH6EAx563iSWSCiaavDHtP2)

## Uso do Projeto

Uma vez que o projeto esteja rodando no Docker Compose, a interface interativa do OpenAPI
estará disponível em http://127.0.0.1:3000/

### Endpoints

O payload para o uso dos verbos POST, PUT e PATCH está listado acima em [Modelos e Serializadores](#modelos-e-serializadores)

#### Profissionais

- GET http://127.0.0.1:3000/api/profissionais - Listagem de profissionais cadastrados
- POST http://127.0.0.1:3000/api/profissionais - Criação de um profissional
- GET http://127.0.0.1:3000/api/profissionais/UUID - Recuperação de dados de um profissional específico
- PUT http://127.0.0.1:3000/api/profissionais/UUID - Atualização total de um profissional específico
- PATCH http://127.0.0.1:3000/api/profissionais/UUID - Atualização parcial de um profissional específico
- DELETE http://127.0.0.1:3000/api/profissionais/UUID - Remoção de um profissional específico

#### Consultas

- GET http://127.0.0.1:3000/api/consultas - Listagem de consultas cadastradas
- GET http://127.0.0.1:3000/api/consultas?profissional_uuid=UUID - Listagem de consultas cadastradas de um profissional em específico
- POST http://127.0.0.1:3000/api/consultas - Criação de uma consulta
- GET http://127.0.0.1:3000/api/consultas/UUID - Recuperação de dados de uma consulta específica
- PUT http://127.0.0.1:3000/api/consultas/UUID - Atualização total de uma consulta específica
- PATCH http://127.0.0.1:3000/api/consultas/UUID - Atualização parcial de uma consulta específica
- DELETE http://127.0.0.1:3000/api/consultas/UUID - Remoção de uma consulta específica

## Dependências do Projeto

- [Python](https://www.python.org/) 3.11+
- [Django](https://www.djangoproject.com/) 4.2 LTS
- [Django REST framework](https://www.django-rest-framework.org/) 3.14
- [django-model-utils](https://github.com/jazzband/django-model-utils) 4.3
- [django-filter](https://github.com/carltongibson/django-filter) 23.5

### Dependências Relacionadas a Banco Relacional

- [psycopg](https://www.psycopg.org/) 3.1
- [dj-database-url](https://github.com/jazzband/dj-database-url) 2.1

### Dependências Relacionadas a Geração de Schema OpenAPI

- [drf-spectacular](https://github.com/tfranzel/drf-spectacular) 0.26

### Dependências Relacionadas a Testes

- [factory_boy](https://github.com/FactoryBoy/factory_boy) 3.3

## Dependências da Solução Integrada

- [PostgreSQL](https://www.postgresql.org/) 16
- [Docker Compose](https://docs.docker.com/compose/)

## Material de referência

- [Docker Compose for Django development](https://til.simonwillison.net/docker/docker-compose-for-django-development): base para o uso de Docker Compose com Django
- [How to (and how not to) design REST APIs](https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs): artigo de opinião sobre design de APIs RESTful
