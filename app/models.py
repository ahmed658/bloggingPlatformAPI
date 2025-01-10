from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, func, UniqueConstraint, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    phone = Column(String(length=20), nullable=True, unique=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    birthdate = Column(Date, nullable=True)
    admin = Column(Boolean, nullable=False, server_default='False')

    # Relationships
    blog_posts = relationship('BlogPost', back_populates='author', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='author', cascade='all, delete-orphan')
    post_likes = relationship('PostsLike', back_populates='user', cascade='all, delete-orphan')
    comment_likes = relationship('CommentsLike', back_populates='user', cascade='all, delete-orphan')


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    like_count = Column(Integer, server_default=text("0"))

    # Relationships
    author = relationship('User', back_populates='blog_posts')
    comments = relationship('Comment', back_populates='blog_post', cascade='all, delete-orphan')
    likes = relationship('PostsLike', back_populates='blog_post', cascade='all, delete-orphan')


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    blog_post_id = Column(Integer, ForeignKey('blog_posts.post_id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    like_count = Column(Integer, server_default=text("0"))

    # Relationships
    author = relationship('User', back_populates='comments')
    blog_post = relationship('BlogPost', back_populates='comments')
    likes = relationship('CommentsLike', back_populates='comment', cascade='all, delete-orphan')


class PostsLike(Base):
    __tablename__ = 'posts_likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    blog_post_id = Column(Integer, ForeignKey('blog_posts.post_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'blog_post_id', name='uq_posts_likes_user_post'),
    )

    # Relationships
    user = relationship('User', back_populates='post_likes')
    blog_post = relationship('BlogPost', back_populates='likes')


class CommentsLike(Base):
    __tablename__ = 'comments_likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.comment_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='uq_comments_likes_user_comment'),
    )

    # Relationships
    user = relationship('User', back_populates='comment_likes')
    comment = relationship('Comment', back_populates='likes')
