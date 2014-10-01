rest-bottle
===========

# Instalação

Instalando o projeto:
---------------------

    git clone git@github.com:yuripiratello/rest-bottle.git
    cd rest-bottle
    pip install -r requirements.txt

Para executar:
--------------

    python run.py
    
Para testar:
------------

    python tests.py
    
Para gerar um relatório de coverage:
------------------------------------

    coverage run run.py
    coverage html
    
Acesse no seu browser o diretório htmlcov que foi gerado pelo coverage.

# Utilização:

Para utilizar execute:

   python run.py
   
# Exemplos:


Incluindo um usuário:
---------------------

    curl -X POST -F facebookId=<facebookID> http://localhost:8388/person/
    
Pesquisando usuários:
---------------------

Para apenas 1 usuário específico:

    curl http://localhost:8388/person/?facebookId=<facebookID>
    
Para todos os usuários:

    curl http://localhost:8388/person/
    
Para limitar o retorno de usuários:

    curl http://localhost:8388/person/?limit=<limite>
    
Para deletar um usuário:

    curl -X DELETE http://localhost:8388/person/<facebookID>/