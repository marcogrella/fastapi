from fastapi import FastAPI
from routers import user, post, auth, vote
from database import engine
#import models
import config
from fastapi.middleware.cors import CORSMiddleware



# como estamos utilizando o alembic para gerenciar a criação das tabelas
# esse bind aqui abaixo foi comentado. 
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # domínios que podem fazer requisição à API ex: "https://www.google.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# roteamento de diferentes controladores 

app.include_router(post.router)  
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# heroku deployment 