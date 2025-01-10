from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, List
from datetime import date, datetime

class UserSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    admin: Optional[bool] = False
    birthdate: Optional[date] = None
    phone: Optional[PhoneNumber] = None

class UserCreate(UserSchema):
    password: str
    root_pass: Optional[str] = None

    
class UserOut(UserSchema):
    user_id: int
    
class UserOutPublic(BaseModel):
    username: str
    first_name: str
    last_name: str
    
class UserEdit(BaseModel):
    username: Optional[str] = None   
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    birthdate: Optional[date] = None
    phone: Optional[PhoneNumber] = None
    password: Optional[str] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class PostBase(BaseModel):
    title: str
    content: str
    
class PostCreate(PostBase):
    pass

class PostReturn(PostBase):
    post_id: int
    created_at: datetime
    updated_at: datetime
    like_count: int
    author: UserOutPublic
    
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentReturn(CommentBase):
    comment_id: int
    blog_post_id: int
    created_at: datetime
    updated_at: datetime
    like_count: int
    author: UserOutPublic
    
class PostLikeBase(BaseModel):
    blog_post_id: int

class PostLikeResponse(BaseModel):
    message: str
    like_count: int

class CommentLikeBase(BaseModel):
    comment_id: int

class CommentLikeResponse(BaseModel):
    message: str
    like_count: int

class UsersWhoLiked(BaseModel):
    users: List[UserOutPublic]