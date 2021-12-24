from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, utils, models, oauth2 
from app.database import get_db 


# objeto para roteamento, utilizado na classe principal.
router = APIRouter(
    prefix="/users",  # cria o prefixo automaticamente em cada endpoint
    tags=['Users'] # cria um grupo para a documentação. http://127.0.0.1:8000/docs
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # criar uma lógica que verifique se um email não está em uso. 
    userDB = db.query(models.User).filter(models.User.email == user.email).first()

    if userDB != None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= f"email {user.email} already in use.")


    #hash do passoword 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) # converte em dicinario e desempacota

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # recupera o valor e devolve atualizado no objeto.
    
    return new_user


@router.get("/{id}",  response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
   user =  db.query(models.User).filter(models.User.id == id).first()

   if user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"user with id: {id} does not exist.")

   return user  