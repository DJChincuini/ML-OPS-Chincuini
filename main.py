from Funciones import *
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero:str):
    '''
    Debe devolver año con mas horas jugadas para dicho género.
    Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
    '''
    try:
        return func_playTime(genero)
    except Exception as e:
        return {"Error":str(e)}
