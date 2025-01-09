from fastapi import FastAPI

blogApp = FastAPI()


@blogApp.get("/")
def root():
    return {"message": "Blog platform test"}