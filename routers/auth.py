from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import schemas, models, utils, oauth2



# objeto para roteamento, utilizado na classe principal.
router = APIRouter(
    prefix="/login",  
    tags=['Authentication'] # cria um grupo para a documentação. http://127.0.0.1:8000/docs
)


@router.post("/")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   
    # verifica se o email da requisição é igual ao email pesquisado na base de dados.
    # o Oauth2 utiliza ao invés de email, o username. Na verdade pouco importa se está comparando com 
    # email na base de dados, apenas utiliza o username como "padrão". Com isso não precisamos 
    # utilizar um corpo na requisição (conforme o schema.UserLogin) e sim enviar no corpo da reqsção
    # utilizando o form-data
    
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Creadentials")

    # verifica se ambos as senhas são iguais 
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Creadentials")

    # gerando o token:
    # obs: no dicionário data é possível colocar no payload o que quiser, o ideal é não por senha.
    access_token = oauth2.create_access_token(data = {"user_id": user.id})


    

    return {"access_token": access_token, "token_type": "bearer"}