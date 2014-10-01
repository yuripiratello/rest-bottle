rest-bottle
===========

Exemplo de API REST feita em [bottlepy](http://bottlepy.org) com unittests e relatório de coverage. 
Sua funcionalidade é bem simples: você envia um post com o Facebook ID ele grava as informações do usuário em um sqlite na memória e disponibiliza outras ações como listagem, exclusão e edição.  

# Configurações

Instalação do projeto:
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