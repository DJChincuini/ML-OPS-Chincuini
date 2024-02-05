import pandas as pd

# Cargo el dataframe
playtime = pd.read_csv('./Datasets/playTimeGenre.csv')
users_gen = pd.read_csv('./datasets/userForGenre.csv')
steam_games = pd.read_csv('./datasets/steam_games.csv')
user_review = pd.read_csv('./datasets/user_reviews.csv')
recom = pd.read_csv('./datasets/sisRecomendacion.csv')


### Función 1 ###
def func_playTime(genero:str):
       
    # Normalizo el input del usuario si este escribe el género en minúsculas o con espacios.    
    genero = genero.strip().capitalize() 
    
    # Si no encuentra el genero retorna un mensaje de error.
    if genero not in playtime['genres'].unique():
        return 'No existe ese género, prueba otro.'  
       
       
    # Filtro la columna genres por el genero y luego busco la mayor cantidad de horas y su año correspondiente.   
    filtro = playtime[playtime['genres'] == genero]
    maximo = filtro.groupby('year')['playtime_forever'].sum().idxmax()
    
    return f'Año de lanzamiento con más horas jugadar por para el genero {genero} es: {maximo}'


### Función 2 ###
def funcUserGenre(genero:str):
    '''
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
    Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    '''
    
     # Saco espacios en blanco y capitalizo la primer letra si es necesario.
    genero = genero.strip().capitalize()
    

    if genero.lower() not in [x.lower() for x in users_gen['Género'].tolist()]:
        return "No se encontró ese genero"
    
     # Busco el genero especificado
    gen = users_gen[users_gen['Género'].str.lower() == genero.lower()]
        
    return { 
        'Usuario':gen['Usuario'].tolist(),
        'Horas jugadas':gen['Año_Horas'].tolist()      
    }



### Función 3 ###
def usersRecommend(año: int):
    ''' Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
    Ejemplo de retorno: ["X", "Y", "Z"]
    '''
    
    if año not in user_review['Año'].unique():
        return 'No se encuentra ningún registro con ese año. Pruebe otro.'
    
    # Filtro por año y reviews positivas
    review_filtered = user_review.loc[(user_review['Año'] == año) & (user_review['sentiment_analysis'] == 2)]
    
    # Encuentro los juegos con más reviews positivas
    conteo = review_filtered.groupby('item_id', as_index=False)['sentiment_analysis'].count().nlargest(3, 'sentiment_analysis')
    
    # Consigo los nombres de los juegos con merge
    conteo = pd.merge(conteo, steam_games[['id', 'app_name']], left_on='item_id', right_on='id', how='outer')
    
    # Creo el diccionario
    dic = [{'Puesto 1': conteo['app_name'].iloc[0]},
           {'Puesto 2': conteo['app_name'].iloc[1]},
           {'Puesto 3': conteo['app_name'].iloc[2]},]
    
    return dic



### Función 4 ###
def usersWorstDeveloper(año: int):
    '''
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
    Ejemplo de retorno: [{"Puesto 1": X}, {"Puesto 2": Y}, {"Puesto 3": Z}]'''
    
    if año not in user_review['Año'].unique():
        return 'No se encuentra ningún registro con ese año. Pruebe otro.'
    
    # Filtro por año y reviews negativas
    review_filtered = user_review.loc[(user_review['Año'] == año) & (user_review['sentiment_analysis'] == 0)]
    
    # Consigo los desarrolladores con merge
    review_negativas = pd.merge(review_filtered, steam_games[['id', 'developer']], left_on='item_id', right_on='id', how='outer')
    
    # Encuentro los desarrolladores con más reviews negativas
    conteo = review_negativas.groupby('developer', as_index=False)['sentiment_analysis'].count().nlargest(3, 'sentiment_analysis')
    
    # Creo el diccionario
    dic = [{'Puesto 1': conteo['developer'].iloc[0]},
           {'Puesto 2': conteo['developer'].iloc[1]},
           {'Puesto 3': conteo['developer'].iloc[2]},]

    return dic



### Función 5 ###
def sentiment(developer:str):
    '''
    Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}
    '''    

    # Saco espacios en blanco y capitalizo la primer letra si es necesario.
    developer = developer.strip().capitalize()


    # Hago un merge entre user_review y steam_games para poder agregar la columna developer al primer dataframe
    user_review = pd.merge(user_review,steam_games[['id','developer']], left_on='item_id',right_on='id', how='inner')


    # Me aseguro de que exista el developer.
    if developer not in user_review['developer'].unique():
        return "No se registran ningun developer con ese nombre. Pruebe otro"
    
    
    # Filtro las reseñas de usuarios para el developer especificado
    reseñas_dev = user_review[user_review['developer'] == developer]

    # Cuento la cantidad de registros para cada categoría de análisis de sentimiento
    conteo_sentimientos = reseñas_dev['sentiment_analysis'].value_counts()

    # 2 = Positive | 1 = Neutral | 0 = Negative
    pos = f'Positive = {conteo_sentimientos[2]}'
    neu = f'Neutral = {conteo_sentimientos[1]}'
    neg = f'Negative = {conteo_sentimientos[0]}'
    
    resultado = {developer:[neg,neu,pos]}

    return resultado



### Modelo de Recomendación ###
def recomendacion(item_id:int):
    
    # Filtrar el DataFrame por el id especificado
    result_df = recom[recom['id'] == item_id]
    
    response_data = result_df.explode('Recomendaciones').astype(str)
    response_data = response_data['Recomendaciones'].apply(lambda x: str(x).replace('[', '').replace(']', '').replace(',', ' -'))
    
    return response_data