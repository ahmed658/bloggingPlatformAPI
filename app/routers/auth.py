from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.services import oauth2_service
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Token
from app.models import User
from app.utils import verify_password

router = APIRouter(
    prefix= "/login",
    tags = ["Authentication"]
)

@router.post("/", response_model=Token)
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == userCredentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not verify_password(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2_service.create_jwt_token(data={"user_id": user.user_id})
    
    return {"access_token": access_token, "token_type": "bearer"}