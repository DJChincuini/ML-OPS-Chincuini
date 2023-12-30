from Funciones import *
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def bienvenida():
    return {'API de consultas a una base de datos de Steam, /docs en el link para acceder a las funciones de consulta.'}

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
    

@app.get("/sentiment_analysis/{año}")
def sentiment_analysis(año:int):
    '''
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados.
    '''
    try:
        return sentiment(año)
    except Exception as e:
        return {"Error":str(e)}
    
    
@app.get("/UsersNotRecommend/{año}")
def UsersNotRecommend(año:int):
    '''
    Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
    '''
    try:
        return notRecommend(año)
    except Exception as e:
        return {"Error":str(e)}


@app.get("/recomendacion_juego/{id_producto}")
def recomendacion_juego(id_producto:int):
    '''
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
    '''
    try:
        return recomendacion(id_producto)
    except Exception as e:
        return {"Error":str(e)}