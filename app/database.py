from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

#import time
#import psycopg2
#from psycopg2.extras import RealDictCursor


# conexão com a base de dados, além de conectar, cria as tabelas.
# OBS: Nunca se coloca informações da base de daddos dessa forma. 


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency, é adicionado para criar uma sessão no bd. Toda a vez que uma requisição é chamada
# utiliza-se esse método abaixo.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# não utilizado mais. Deixado somente para documentação. Utilizado para gerar as consultas de forma
# direta no bd.
 
# while True:
    #try:
        #conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', 
        #password='admin', cursor_factory=RealDictCursor)
        #cursor = conn.cursor()
        #print("Database connection wass sucessfull!")
        #break
    #except Exception as error:
        #print("Connection to database failed")
        #print("Error: ", error)
        #time.sleep(2)