from fastapi import FastAPI

blogApp = FastAPI()


@blogApp.get("/")
async def root():
    return {"message": "Blog platform test"}