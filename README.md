# Fast Api do Zero: Projeto Final

Projeto final do curso Fast Api do Zero do Dunossauro [link do curso](https://fastapidozero.dunossauro.com).

## Projeto

O projeto se chama MADR (Meu Acervo Digital de Romances). No projeto cada usuário possui uma **conta** (protegida pro e-mail/senha). Depois que está "dentro" da conta (ou seja, authenticado com um JWT), o usuário pode criar/ler/atualizar/excluir **romancistas** e **livros** que queira guardar no acervo. Diferentemente do que foi proposto no curso, cada usuário possui um acervo pessoal, somente acessível por sua conta.

## Ferramentas Utilizadas

- Linguagem de programação: Python 3.12
- Banco de dados: PostgreSQL 16

## Pacotes Python Utilizados

- fastAPI: servidor de aplicação
- pydantic: schemas para validar entrada e saída da aplicação
- psycopg: driver para PostgreSQL
- sqlalchemy: ORM para interagir com o banco de dados
- pydantic-settings: para ler o arquivo .env com tipagem
- alembic: para gerar e gerir migrações no banco de dados
- pyjwt: gerar, validar e decodificar JWTs
- pwdlib: gerar e validar hash de senhas
- bleach: sanitizar tags script

### Dependências de desenvolvimento

- pytest: executar testes unitários de da aplicação
- pytest-cov: gerar cobertura de testes
- factory-boy: gera factories para os testes
- taskipy: comandos rápidos para desenvolvimento
- ruff: linter, formatador e mais
- freezegun: viagem no tempo para testes
- testcontainers: gerenciar containers durante os testes

## Instalação

### Com docker-compose

```sh
docker-compose up
```

### Sem docker-compose

Primeiro instale o PostgreSQL 16 na porta 5432. Depois instale o python 3.12. Com o python 3.12 instalado, execute os comandos:

```sh
pip install pipx
pipx install poetry
poetry install
poetry run alembic upgrade head
poetry poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero_projeto_final.app:app
```

## Desenvolvimento

- Em um terminal, execute `poetry shell`
- Depois execute `task postgres_up`
- Em outro terminal, execute `poetry shell`
- Depois execute `task run`