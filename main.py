from Funciones import *
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def bienvenida():
    return {'API de consultas a una base de datos de Steam, /docs en el link para acceder a las funciones de consulta.'}


@app.get('/PlayTimeGenre/{genero}')
def PlaytimeGenre(genero:str):
    try:
        return func_playTime(genero)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UserForGenre/{genero}')
def UserForGenre(genero:str):
    try:
        return funcUserGenre(genero)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UsersRecommend/{año}')
def UsersRecommend(año:int):
    try:
        result = usersRecommend(año)
        return result
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UserWorstDeveloper/{año}')
def UserWorstDeveloper(año:int):
    try:
        result = usersWorstDeveloper(año)
        return result
    except Exception as e:
        return {"Error":str(e)}


@app.get('/sentiment_analysis/{developer}')
def sentiment_analysis(developer:str):
    try:
        return sentiment(developer)
    except Exception as e:
        return {"Error":str(e)}
    
    
@app.get('/recomendacion_juego/{id}')
def recomendacion_juego(item_id:int):
    try:
        return recomendacion(item_id)
    except Exception as e:
        return {"Error":str(e)}