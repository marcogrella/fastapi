from fastapi.param_functions import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session
from app import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import settings


# tokenUrl é o endpoint do login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# token possui 3 partes:

# Secret_key
# Algoritimo
# Expiration time

# OBS: essa chave não se expõe dessa forma. Para isso fazemos o uso de variáveis de ambiente e esses dados
# ficam na máquna local
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()   # recebe um dicionario e copia o conteúdo no novo dic chamado to_encode

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # adiciona essa propriedade no dicionario

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# OBS: basicamente, para cada endpoint que queremos que se faça a verificação por token, devemos
# utilizar a validação via token, ou seja, para que um endpoint seja executado, é necessário que 
# o usuário possua um token válido (tenha logado anteriormente e obtido um token)


# funcao para verificar a autenticidade do token

def verify_access_token(token: str, credentials_exception):

    try: 

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # pegamos uma parte do token (user_id). Essa info é quando geramos o token. 
        # Extraímos o id:
        id: str = payload.get("user_id")

        if id is None: 
            raise credentials_exception  # levanta a exceção informada. 
        
        token_data = schemas.TokenData(id=id) # jogamos o id em um modelo. Podemos retornar além do id (varia de acordo com as regras de negócio)

    except JWTError:
        raise credentials_exception  
    
    return token_data

# funcao para verificar o usuário atual

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db) ):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    # requisição na base de dados e retornar o usuário com base no id que é carregado no token :
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user