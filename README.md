# **saude-drf** Desafio Lacrei Saúde Back end

Repositório de [Alexandre Harano](mailto:email@ayharano.dev)


## Instalação

Após [a instalação de Docker Compose](https://docs.docker.com/compose/install/), utilizando um terminal, vá para a raiz deste projeto e rode

```shell
$ docker compose web up
```

para rodar o projeto Django com o banco de dados PostgreSQL.

O container da aplicação possui um usuário não-root na distribuição Debian e é usado um ambiente virtual de Python 3.11. Desta forma, não é necessária a instalação de um ambiente virtual local.

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
