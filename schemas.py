
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

# classes PostBase utiliza validação de dados do BaseModel, determina o comportamento do corpo da requisicao
# A classe PostCreate recebe campos por herança

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None  # quando um campo é opcional

class PostCreate(PostBase):
    pass
 

#resposta
class UserResponse(BaseModel):
    id: int
    email: EmailStr  # validador do pydantic
    created_at: datetime
    
    class Config:      
         orm_mode = True


# classe para a resposta da requisição. Util para mostrar somente os dados necessarios (response_model): 

class Post(PostBase):  # herança
     id: int
     created_at: datetime
     user_id: int
     user: UserResponse   # faz a relação entre o post e o usuário

     # necessario porque a classe do Pydantic model só trabalha default com dict.
     class Config:      
         orm_mode = True


# resposta para o número de votos por posts

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:      
         orm_mode = True



# requisicao
class UserCreate(BaseModel):
    email: EmailStr
    password: str




# requisicao para login (não utilizado)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str  

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    # importa do pydantic e só permite valores positivos. Esse dir é só para dizer se queremos excluir
    # o voto em um post. Se for 1 
    dir: conint(le=1) 


