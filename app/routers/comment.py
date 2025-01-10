from fastapi import HTTPException, status, Depends, APIRouter, Response
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas
from app.services import oauth2_service
from ..database import get_db

router = APIRouter(
    prefix = "/comments",
    tags=["Comments"]
)

@router.post("/posts/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentReturn)
def create_comment(comment: schemas.CommentCreate, post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2_service.get_current_user)):
    post = db.query(models.BlogPost).filter(models.BlogPost.post_id == post_id).first()
    if not post:
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail=f"Blog post with ID {post_id} was not found."
         )
    new_comment = models.Comment(content=comment.content, user_id=current_user.user_id, blog_post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/posts/{post_id}", response_model=List[schemas.CommentReturn])
def get_comments_of_post(post_id: int, db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    post = db.query(models.BlogPost).filter(models.BlogPost.post_id == post_id).first()
    if not post:
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail=f"Blog post with ID {post_id} was not found."
         )
    comments = db.query(models.Comment).filter(models.Comment.blog_post_id == post_id)
    comments = comments.limit(limit).offset(skip).all()
    return comments

@router.get("/{id}", response_model=schemas.CommentReturn)
def get_comment(id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.comment_id == id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {id} was not found."
        )
    return comment

@router.put("/{id}", response_model=schemas.CommentReturn)
def update_comment(id: int, updated_comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2_service.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with ID {id} was not found")
    if comment.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Comment with ID {id} doesn't belong to the current user.")

    comment_query.update(updated_comment.model_dump(), synchronize_session=False)
    db.commit()
    return comment_query.first()

@router.delete("/{id}")
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2_service.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with ID {id} was not found")
    if comment.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Comment with ID {id} doesn't belong to the current user.")

    comment_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
