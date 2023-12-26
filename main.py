from Funciones import *
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero:str):
    try:
        return func_playTime(genero)
    except Exception as e:
        return {"Error":str(e)}
