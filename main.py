from Funciones import *
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def bienvenida():
    return {'API de consultas a una base de datos de Steam, /docs en el link para acceder a las funciones de consulta.'}


@app.get('/PlayTimeGenre/{genero}')
def func_playTime(genero:str):
    try:
        return func_playTime(genero)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UserForGenre/{genero}')
def funcUserGenre(genero:str):
    try:
        return funcUserGenre(genero)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UsersRecommend/{año}')
def func_UsersRecommend( año : int ):
    try:
        return func_UsersRecommend(año)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UsersWorstDeveloper/{año}')
def func_UsersWorstDeveloper( año : int ):
    try:
        return func_UsersWorstDeveloper(año)
    except Exception as e:
        return {"Error":str(e)}
    
    
    
@app.get('/sentiment_analysis/{developer}')
def sentiment(developer:str):
    try:
        return sentiment(developer)
    except Exception as e:
        return {"Error":str(e)}
    
    
@app.get('/recomendacion_juego/{id}')
def recomendacion(id_producto:int):
    try:
        return recomendacion(id_producto)
    except Exception as e:
        return {"Error":str(e)}