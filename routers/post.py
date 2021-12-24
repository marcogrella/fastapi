from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas, oauth2 
from app.database import get_db



# objeto para roteamento, utilizado na classe principal.
router = APIRouter(
    prefix="/posts",  # cria o prefixo automaticamente em cada endpoint
    tags=['Posts'] # cria um grupo para a documentação. http://127.0.0.1:8000/docs
)

# limit é um parâmetro opcional. No caso para enviar esse parâmetro, na requisição basta colocar o ?
# ficando url/posts?limit=3 esse parâmetro é útil para filtrar depois. 
# Da mesma maneira com o skip.  url/posts?limit=5&skip=2 
# e do search Ex: {{URL}}posts?limit=5&skip=0&search=java (filtra tudo que há no título)
# coloca-se o % no meio das palavras ficando tipo {{URL}}posts?limit=5&search=java%1





@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #posts = db.query (models.Post).limit(limit).offset(skip).all()
    #posts = db.query(models.Post).limit(limit).all()
    #posts = db.query(models.Post).all() 

    # faz a busca somente dos posts que pertencem ao usuario
    #posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all() 
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join( 
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

    return posts


@router.get("/votes", response_model=List[schemas.PostOut])
def get_posts_by_votes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # consulta os posts relacionando com a quantidade de votos

    # como opção podemos filtrar utilizando as opções conforme utilizamos nas buscas:

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    return results
 


# response_model -> faz uso da classe criada para resposta.

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # importamos o modelo (que representa a tabela), em seguida faz-se a conversão entre objeto de entrada e modelo
    
    # abaixo é uma forma não ideal de colocar os dados de um objeto em outro
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    print(f'Quem fez a alteração foi o usuário: {current_user.email}')

    # aqui utiliza-se o id do que está criando o post (current_user.id) e associa automaticamente no post (user_id que a fk)
    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post) # recupera o valor e devolve atualizado no objeto.
    
    return new_post


#@router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #post = db.query(models.Post).filter(models.Post.id == id).first() # retorna o antigo.
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    
    #if post.user_id != current_user.id:
      # raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
      # detail=f'Not authorized to perform requested action')
    
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist.")
    

    # o usuário só poderá excluir um post que for de autoria dele. 

    if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
        detail=f'Not authorized to perform requested action')
    

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updt_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
     post_query = db.query(models.Post).filter(models.Post.id == id)
     post = post_query.first()   
     
     if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist.")
     
     if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
        detail=f'Not authorized to perform requested action')

     post_query.update(updt_post.dict(), synchronize_session=False)
     db.commit()

     return post_query.first()