from fastapi import HTTPException, status, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.services import oauth2_service
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2_service.get_current_user)):
    newPost = models.BlogPost(**post.model_dump(), user_id= current_user.user_id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.get("/", response_model=List[schemas.PostReturn])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return db.query(models.BlogPost).filter(models.BlogPost.content.contains(search)).limit(limit).offset(skip)

@router.get("/{id}", response_model=schemas.PostReturn)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.BlogPost).filter(models.BlogPost.post_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found.")
    return post

@router.put("/{id}", response_model=schemas.PostReturn)
def update_post(id: int, editedPost: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2_service.get_current_user)):
    post_query = db.query(models.BlogPost).filter(models.BlogPost.post_id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"post with ID {id} was not found")
    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Post with ID {id} doesn't belong to the current user to edit it.")
    post_query.update(editedPost.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2_service.get_current_user)):
    post_query = db.query(models.BlogPost).filter(models.BlogPost.post_id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"post with ID {id} was not found so it was not deleted.") 
        
    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Post with ID {id} doesn't belong to the current user to delete it.")
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)