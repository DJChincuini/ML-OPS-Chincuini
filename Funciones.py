import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split


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


### Función 2 ###
def sentiment(año:int):
    
    # Cargo el DataFrames.
    user_review = pd.read_csv('./datasets/user_reviews.csv')

    # Me aseguro de que exista el año.
    if año not in user_review['Año'].unique():
        return "No se registran ningun juego ese año. Pruebe otro"
    
    # Filtro las reseñas de usuarios para el año especificado
    reseñas_año = user_review[user_review['Año'] == año]

    # Cuento la cantidad de registros para cada categoría de análisis de sentimiento
    conteo_sentimientos = reseñas_año['sentiment_analysis'].value_counts()

    # Creo un diccionario con el conteo de sentimientos
    resultado = {
        'Negative': conteo_sentimientos.get('Negative', conteo_sentimientos[0]),
        'Neutral': conteo_sentimientos.get('Neutral', conteo_sentimientos[1]),
        'Positive': conteo_sentimientos.get('Positive', conteo_sentimientos[2])
    }

    return resultado


### Función 3 ###
def notRecommend(año: int):
    # Cargo los DataFrames.
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    
    # Me aseguro de que exista el año.
    if año not in user_review['Año'].unique():
        return "No se registran ningun juego ese año. Pruebe otro"
    
    # Filtrar las revisiones para el año dado y donde la recomendación es False y el análisis de sentimientos es negativo
    filtered_reviews = user_review[(user_review['Año'] == año) & (user_review['recommend'] == False) & (user_review['sentiment_analysis'] <= 1)]

    # Agrupar por item_id y contar las revisiones para cada juego
    game_counts = filtered_reviews.groupby('item_id')['user_id'].count().reset_index(name='count')

    # Combinar con el DataFrame steam_games para obtener información adicional
    games_info = pd.merge(game_counts, steam_games[['id', 'app_name']], how='left', left_on='item_id', right_on='id')

    # Ordenar los juegos por la cantidad de revisiones en orden ascendente
    sorted_games = games_info.sort_values(by='count', ascending=True)

    # Tomar los tres juegos menos recomendados
    top_3_least_recommended = sorted_games.head(3)

    # Crear la lista de resultados en el formato deseado
    result_list = [{"Puesto {}".format(i + 1): row['app_name']} for i, row in top_3_least_recommended.iterrows()]

    return result_list


### Función 4 ###
def recomendacion(id_producto):
    
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    user_items = pd.read_csv(f'./datasets/user_items_comp_csv.gz', compression='gzip') 
    user_review = pd.read_csv('./datasets/user_reviews.csv')

    # Creo los DF necesarios.
    df = steam_games.drop(columns=['price', 'developer'])
    df['playtime'] = user_items.sort_values('id')['playtime_forever'].sum()
    df[['recommend','sentiment_analysis	']] = user_review.sort_values('item_id')[['recommend', 'sentiment_analysis']]
    df = df.dropna()

    features = steam_games.drop(columns=['genres', 'app_name', 'price', 'developer','Year'])


    # Construyo el conjunto de datos de entrenamiento
    X_train, X_test = train_test_split(features, test_size=0.2, random_state=42)

    # Entrenamiento
    knn_model = NearestNeighbors(n_neighbors=6, algorithm='auto').fit(X_train)

    
    # Encuentro el índice correspondiente al ID del producto en el conjunto de entrenamiento
    indice_producto = features.index[features['id'] == id_producto].tolist()[0]

    # Encuentro los vecinos más cercanos usando el modelo KNN
    _, indices_vecinos = knn_model.kneighbors(features.iloc[indice_producto].values.reshape(1, -1))

    # Obtengo los IDs de los juegos recomendados
    juegos_recomendados = features.iloc[indices_vecinos[0][1:]]['id'].tolist()
    
    # Creo una máscara booleana para seleccionar las filas con los IDs en la lista
    mask = steam_games['id'].isin(juegos_recomendados)

    # Filtro el DataFrame usando la máscara
    resultados = steam_games[mask]

    # Obtengo las columnas 'id' y 'app_name' de los resultados
    ids_encontrados = resultados['id']
    nombres_encontrados = resultados['app_name']


    for id_, nombre in zip(ids_encontrados, nombres_encontrados):
        print(f"ID: {id_}, Nombre: {nombre}")