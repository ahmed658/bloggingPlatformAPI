from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.schemas import UserCreate, UserOut, UserEdit
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import hash_password, remove_attribute, verify_password
from app.models import User
from app.services import oauth2_service
from app.config import settings
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_details: UserCreate, db: Session = Depends(get_db)):
    if user_details.admin and user_details.root_pass != settings.root_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to create an admin user unless you have the master root password")
    
    user_details = remove_attribute(user_details, "root_pass")
    user_details.password = hash_password(user_details.password)
    newUser = User(**user_details.model_dump())
    try:
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Duplicate entry")
    
@router.put("/", response_model=UserOut)
def update_current_user(user_details: UserEdit, current_user = Depends(oauth2_service.get_current_user), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.user_id == current_user.user_id)
    if user_details.password != None:
        user_details.password = hash_password(user_details.password)
    user_details_to_add = {}
    for field, value in user_details.model_dump().items():
        if value != None:
            user_details_to_add[field] = value
    user_query.update(user_details_to_add, synchronize_session=False)
    db.commit()
    return user_query.first()

@router.put("/{username}", response_model=UserOut)
def update_user(username: str, user_details: UserEdit, current_user = Depends(oauth2_service.get_current_user), db: Session = Depends(get_db)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Only admins are allowed to edit other users")
    
    user_query = db.query(User).filter(User.username == username)
    
    userToEdit = user_query.first()
    if not userToEdit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You are trying to edit user {username} which does not exist")
    
    
    if user_details.password != None:
        user_details.password = hash_password(user_details.password)
        
    user_details_to_add = {}
    for field, value in user_details.model_dump().items():
        if value != None:
            user_details_to_add[field] = value
            
    user_query.update(user_details_to_add, synchronize_session=False)
    db.commit()
    return user_query.first()

@router.get("/", response_model=List[UserOut])
def get_users(current_user = Depends(oauth2_service.get_current_user), db: Session = Depends(get_db)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins are allowed to list other users")
    
    return db.query(User).all()

@router.delete("/")
def remove_account(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.username == userCredentials.username)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not verify_password(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    user_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{username}")
def remove_user(username: str, current_user = Depends(oauth2_service.get_current_user), db: Session = Depends(get_db)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Only admins are allowed to delete other users") 
      
    user_query = db.query(User).filter(User.username == username)
    userToDelete = user_query.first()
    if not userToDelete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You are trying to delete {username} which does not exist")
    
    user_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)