from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.services import oauth2_service
from ..database import get_db
from app import models, schemas
from typing import List

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post("/posts/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostLikeResponse)
def like_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2_service.get_current_user)):
    post = db.query(models.BlogPost).filter(models.BlogPost.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} does not exist."
        )

    existing_like = db.query(models.PostsLike).filter(
        models.PostsLike.blog_post_id == post_id,
        models.PostsLike.user_id == current_user.user_id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have already liked post {post_id}."
        )
    
    new_like = models.PostsLike(blog_post_id=post_id, user_id=current_user.user_id)
    post.like_count += 1
    db.add(new_like)
    db.commit()
    db.refresh(post)

    return schemas.PostLikeResponse(
        message=f"Post {post_id} liked successfully.",
        like_count=post.like_count
    )


@router.delete("/posts/{post_id}", response_model=schemas.PostLikeResponse)
def unlike_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2_service.get_current_user)):
    post = db.query(models.BlogPost).filter(models.BlogPost.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} does not exist."
        )

    like_query = db.query(models.PostsLike).filter(
        models.PostsLike.blog_post_id == post_id,
        models.PostsLike.user_id == current_user.user_id
    )
    existing_like = like_query.first()
    if not existing_like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You haven't liked post {post_id}."
        )

    like_query.delete()
    post.like_count -= 1
    db.commit()
    db.refresh(post)

    return schemas.PostLikeResponse(
        message=f"Post {post_id} unliked successfully.",
        like_count=post.like_count
    )


@router.post("/comments/{comment_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentLikeResponse)
def like_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2_service.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} does not exist."
        )

    existing_like = db.query(models.CommentsLike).filter(
        models.CommentsLike.comment_id == comment_id,
        models.CommentsLike.user_id == current_user.user_id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have already liked comment {comment_id}."
        )

    new_like = models.CommentsLike(comment_id=comment_id, user_id=current_user.user_id)
    comment.like_count += 1
    db.add(new_like)
    db.commit()
    db.refresh(comment)

    return schemas.CommentLikeResponse(
        message=f"Comment {comment_id} liked successfully.",
        like_count=comment.like_count
    )


@router.delete("/comments/{comment_id}", response_model=schemas.CommentLikeResponse)
def unlike_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2_service.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} does not exist."
        )

    like_query = db.query(models.CommentsLike).filter(
        models.CommentsLike.comment_id == comment_id,
        models.CommentsLike.user_id == current_user.user_id
    )
    existing_like = like_query.first()
    if not existing_like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You haven't liked comment {comment_id}."
        )

    like_query.delete()
    comment.like_count -= 1
    db.commit()
    db.refresh(comment)

    return schemas.CommentLikeResponse(
        message=f"Comment {comment_id} unliked successfully.",
        like_count=comment.like_count
    )

@router.get("/posts/{post_id}/users", response_model=List[schemas.UserOutPublic])
def get_users_who_liked_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2_service.get_current_user), limit: int = 10, skip: int = 0):
    post = db.query(models.BlogPost).filter(models.BlogPost.post_id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} does not exist."
        )

    user_query = db.query(models.User).join(models.PostsLike, models.PostsLike.user_id == models.User.user_id).filter(models.PostsLike.blog_post_id == post_id)

    users = user_query.offset(skip).limit(limit).all()

    return users

@router.get("/comments/{comment_id}/users", response_model=List[schemas.UserOutPublic])
def get_users_who_liked_comment(comment_id: int, db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    comment = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} does not exist."
        )

    user_query = db.query(models.User).join(
        models.CommentsLike, models.CommentsLike.user_id == models.User.user_id
    ).filter(
        models.CommentsLike.comment_id == comment_id
    )

    users = user_query.offset(skip).limit(limit).all()

    return users