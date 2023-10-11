<p>
 <img width="300" src="https://github.com/SrTorpedro/PI-SB-Animais/blob/main/static/imgs/logo.png?raw=true" />
 <h2 align="">AdotPet</h2>
 <p align="">Uma plataforma facilitadora de adoção de animais!</p>

# :memo: Visão Geral

Aplicação desenvovida para ser um facilitador na adoção de animais.


 * <strong><a href="#description">Descrição completa do sistema</a></strong>
 * <strong><a href="#tecnologias">Tecnologias utilizadas</a></strong>
 * <strong><a href="#requisitos">Pré-requisitos</a></strong>
 * <strong><a href="#docker">Instalando o Docker</a></strong>
 * <strong><a href="#django">Como executar o programa no Django</a></strong>
 * <strong><a href="#screenshots">Screenshots</a></strong>
 
# PI-SB-Animais

## Instalando o Docker

Execute o seguinte código no Terminal na pasta raíz do projeto:

**Lembre de ter o Docker ou Docker Desktop instalado na máquina.** :shipit:

`docker build -t pi-animais .`

Aguarde a imagem do Docker ser construída.

Após isso execute o seguinte código para a criação do Container:

`venv/Scripts/activate.ps1`
`docker compose up`

## Como executar o programa no Django

**Iniciar venv.**

`python -m venv venv .`

**Ativar venv.**

`venv/Scripts/Activate.ps1`

**Desativar venv.**

`deactivate`

Com a venv ativada:

**Instalação de dependências**

`pip install django`
`pip install pillow`
`pip freeze > requeriments.txt`

Agora para fazer as migrações no banco de dados:

`python manage.py makemigrations`
`python manage.py migrate`

**Executar o projeto**

`python manage.py runserver`
