from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token 
from app import models


# esse arquivo ajuda a definir as fixtures e tornam acessíveis em quaiquer arquivos do pacote, o bom é que as 
# fixtures session, client, text_users e etc  podem ser importadas automaticamente




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
    #print("Fixture of session")
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



@pytest.fixture() 
def client(session): # note que agora um fixture depende do outro.
    #return TestClient(app) # antigo
    #print("fixture of client")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()


    #  aqui se realiza o override do get_db e com isso toda a vez que o método que estiver sendo executado 
    # para teste irá sobrescrever o get_db de modo que não precisamos ficar alterando o código nos métodos 
    # get, post, delete, put

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    

# auxilia na criação de um usuário no bd para fazer o login

@pytest.fixture
def test_user(client):
    user_data = {"email": "admin@email.com", "password": "admin"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user_2(client):
    user_data = {"email": "admin_2@email.com", "password": "admin_2"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


# aqui pegamos o client original e inserimos no header o token. 
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
         "title": "2° title",
        "content": "second content",
        "user_id": test_user['id']
    } , {
         "title": "3° title",
        "content": "third content",
        "user_id": test_user['id']
    } , {
         "title": "4° title",         # pertence ao usuário 2
        "content": "fourth content",
        "user_id": test_user_2['id']

    }]

    # função para converter, para cada item de um dicionario, objetos do tipo Post para salvar no bd
    def create_post_model(post):
        return models.Post(**post) # pega cada item (chave / valor e converte para Post)

    post_map = map(create_post_model, posts_data) # não retorna exatamente uma lista   
    posts = list(post_map) # converte map para lista 
    session.add_all(posts)


    # método que funciona, mas foi comentado. 
    #session.add_all([models.Post(title="first title", content="first content", user_id = test_user['id']),
                    #models.Post(title="2nd title", content="second content", user_id = test_user['id']),
                   # models.Post(title="3rd title", content="third content", user_id = test_user['id']),
                    #]) 
    session.commit()
    posts = session.query(models.Post).all()
    return posts