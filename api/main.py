from fastapi import FastAPI
from routers import clues

app = FastAPI()

app.include_router(clues.router)

@app.get("/")
async def root():
    return {"message": "API up"}