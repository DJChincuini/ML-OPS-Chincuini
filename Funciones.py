import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


### Función 1 ###
def func_playTime(genero:str):
    
    # Cargo los DataFrames.
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    
    user_review = pd.read_csv('./datasets/user_reviews.csv')
   
    user_items = pd.read_csv(f'./datasets/user_items_comp_csv.gz', compression='gzip') 
    
    # Creo un DataFrame con las columnas necesarias.
    horas = user_items.groupby('id')['playtime_forever'].sum().reset_index()
    horas['genres'] = steam_games.sort_values(by='id')['genres']
    horas['genres'] = horas['genres'].str.split('.')
    horas['year'] = user_review.sort_values(by='item_id')['Año']


    genero = genero.strip().capitalize() # Normalizo el input del usuario si este escribe el género en minúsculas o con espacios.
    explode = horas.explode('genres') # Separo cada uno de los generos de la columna genres.
    
    
    # Si no encuentra el genero retorna un mensaje de error.
    if genero not in explode['genres'].unique():
        return 'No existe ese género, prueba otro.'  
       
       
    # Filtro la columna genres por el genero y luego busco la mayor cantidad de horas y su año correspondiente.   
    filtro = explode[explode['genres'] == genero]
    maximo = filtro.groupby('year')['playtime_forever'].sum().idxmax()
    
    return f'Año de lanzamiento con más horas jugadar por para el genero {genero} es: {maximo}'