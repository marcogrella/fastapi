from sqlalchemy import Boolean, Integer, String, Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base




# models aqui representam as tabelas no banco de dados.
# os valores dentro das colunas são imports sqlalchemy
# A cada reinicio da Api, essa tabela é criada. Se houver alteração não atualiza automaticamente.


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #referencia da tabela users
    
    # para mostrar em vez de user_id apresentar o nome ou email de quem pertence o post
    # cria uma relação de forma automática (não impacta ou cria uma coluna a mais). Com isso
    # configura-se a classe PostRequest e no Post inserimos o campo user: UserResponse 
    user = relationship("User")  


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# classe modelo POST utiliza chave composta (cada usuário poderá votar somente uma vez em cada post)
# sendo assim, irá possuir um post_id e user_id

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id",  ondelete="CASCADE"), primary_key=True, nullable=False)

