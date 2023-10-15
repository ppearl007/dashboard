from fastapi import FastAPI
from server.routes.item import router as ItemRouter


app = FastAPI()

app.include_router(ItemRouter, tags=["Item"], prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the CTB app!"}
