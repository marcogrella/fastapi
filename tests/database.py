from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base




################# definindo a base de dados para testes #####################

# nesta configuração, fazemos o uso de um banco de testes. Além disso fazemos o uso do override que sobrescreve o get_db para o override_get_db 

# url de conexão para testes (tem o _test no final que indica fastapi_teste):
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


##############################################################################################

# o escopo do fixture nesse caso executa é para executar o session no final dos testes. 

# escopos: 

# function: the default scope, the fixture is destroyed at the end of the test.
# class: the fixture is destroyed during teardown of the last test in the class
# module: the fixture is destroyed during teardown of the last test in the module.
# package: the fixture is destroyed during teardown of the last test in the package.
# session: the fixture is destroyed at the end of the test session.


@pytest.fixture() 
def session():
    print("Fixture of session")
    # aqui a ideia é recriar as tabelas antes de executar os testes.
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


    # podemos utilizar o alembic nesse método:
    # command.upgrade("head")
    # command.downgrade("base")


# agora toda a vez que utilizamos esse client, o 
# client = TestClient(app) # utilizamos o @pytest.fixture


@pytest.fixture() 
def client(session): # note que agora um fixture depende do outro.
    #return TestClient(app) # antigo
    print("fixture of client")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()


    #  aqui se realiza o override do get_db e com isso toda a vez que o método que estiver sendo executado 
    # para teste irá sobrescrever o get_db de modo que não precisamos ficar alterando o código nos métodos 
    # get, post, delete, put que fazemo o uso do get_db 

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    


