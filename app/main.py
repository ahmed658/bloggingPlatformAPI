from fastapi import FastAPI
from app.routers import user, auth, post, comment, like

blogApp = FastAPI()


blogApp.include_router(user.router)
blogApp.include_router(auth.router)
blogApp.include_router(post.router)
blogApp.include_router(comment.router)
blogApp.include_router(like.router)