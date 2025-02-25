Projeto: 
Venda de sandalias

diagrama de entidades:

modo de usar:
para iniciar o projeto deve-se fazer:
ter o Uv instalado para baixar as dependencias do projeto,
na pasta rais do projeto dar os seguntes comandos:
uv venv --python3.12

source .venv/bin/activate

uv install pip pyproject.toml

deve-se também ter uma variavel de ambiente:

//para banco de dados NoSQL
DATABASE_URL="mongo+srv:user:pass@host"

apos isso basta executar esse comando:
fastapi dev main.py