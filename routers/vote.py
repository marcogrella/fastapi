from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oauth2 
from app.database import get_db



router = APIRouter(
    prefix="/vote", 
    tags=['Vote'] 
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)):
    
    # verifica se o post existe:
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Vote with {vote.post_id} does not exist" )

    # faz a busca para verificar se o voto já existe com o usuário que está tentando votar. 
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if(vote.dir == 1):  # dir == 1 diz que quer adicionar um voto em um post
        if found_vote:  # se já houver um voto (não pode repetir)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        # adiciona o voto se não existir
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)  # seta o voto
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}