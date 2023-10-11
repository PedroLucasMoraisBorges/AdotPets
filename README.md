<p>
 <img width="300" src="https://github.com/SrTorpedro/PI-SB-Animais/blob/main/static/imgs/logo.png?raw=true" />
 <h2 align="">🐶 AdotPet 🐱</h2>
 <p align="">Uma plataforma facilitadora de adoção de animais!</p>

# PI-SB-Animais

# :memo: Visão Geral

Aplicação desenvovida para ser um facilitador na adoção de animais.


 * <strong><a href="#description">Descrição completa do sistema</a></strong>
 * <strong><a href="#tecnologias">Tecnologias utilizadas</a></strong>
 * <strong><a href="#requisitos">Pré-requisitos</a></strong>
 * <strong><a href="#docker">Instalando o Docker</a></strong>
 * <strong><a href="#django">Como executar o programa no Django</a></strong>
 * <strong><a href="#screenshots">Screenshots</a></strong>

<h1 id="description">:speech_balloon: Descrição</h1>

**Trata-se do desenvolvimento de uma aplicação para facilitar a comunicação entre quem possui um animal para adoção com quem deseja adotar.**

Há algumas regras que devem ser seguidas para que alguém possa publicar um animal ou para que alguém possa adotar um animal.

**Regras para quem deseja publicar um animal para adoção:**
 * Primeiramente a pessoa deve estar logada, caso contrário deve-se criar um perfil;
 * A pessoa precisa fornecer os dados de contato;
 * Não pode ter dois ou mais bloqueios de publicações;
 
**Regras para quem deseja adotar um animal:**
 * Primeiramente a pessoa deve estar logada, caso contrário deve-se criar um perfil;
 * A pessoa precisa fornecer os dados de contato;
 * Precisa fazer o pedido de adoção ao dono do animal.

O sistema deve possuir alguma forma de controle de publicações onde haverá os usuários moderadores e os administradores, cada um desses terão poderes diferentes dentro do sistema.

**Poderes do moderador:**
 * Pode modificar descrições de postagens de outras pessoas;
 * Pode bloquear uma postagem (Nesse caso o moderador deverá explicar o motivo e se for falsa comunicação o moderador perderá o poder);
 * O moderador pode desbloquear postagens de outras pessoas.

**Poderes do administrador:**
O administrador possui todos os poderes do moderador, o mais seguro é haver apenas um administrador, que será o responsável por todos os moderadores, o único poder que o administrador tem a mais do que o moderador é a capacidade de tirar o poder de moderador.

"*Os bloqueios são essenciais para o sistema para garantir que ninguém irá utilizar a plataforma para publicações fora de contexto, portanto, se dois bloqueios forem aplicados em um perfil o mesmo será bloqueado.*"
 
<br>

<h1 id="tecnologias">:rocket: Tecnologias utilizadas</h1>

<br>

* <img alt="Python" src="https://img.shields.io/badge/-Python-green"> - Linguagem de programação utilizada no desenvolvimento Back-end.
* <img alt="Django" src="https://img.shields.io/badge/-Django-green"> - Framework utilizado.

<h1 id="docker">:information_source: Instalando o Docker</h1>

Execute o seguinte código no Terminal na pasta raíz do projeto:

**Lembre de ter o Docker ou Docker Desktop instalado na máquina.** :shipit:

`docker build -t pi-animais .`

Aguarde a imagem do Docker ser construída.

Após isso execute o seguinte código para a criação do Container:

`venv/Scripts/activate.ps1`
`docker compose up`

<h1 id="django">:warning: Como executar o programa no Django</h1>

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
