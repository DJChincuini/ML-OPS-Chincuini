import pandas as pd
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
def funcUserGenre(genero:str):
    '''
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
    Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    '''
    
     # Saco espacios en blanco y capitalizo la primer letra si es necesario.
    genero = genero.strip().capitalize()
    
    # Cargo el csv de los generos con usuarios con mas horas
    users_gen = pd.read_csv('./datasets/userForGenre.csv')
    if genero.lower() not in [x.lower() for x in users_gen['Género'].tolist()]:
        return "No se encontró ese genero"
    
     # Busco el genero especificado
    gen = users_gen[users_gen['Género'].str.lower() == genero.lower()]
        
    return { 
        'Usuario':gen['Usuario'].tolist(),
        'Horas jugadas':gen['Año_Horas'].tolist()      
    }


### Función 3 ###
def func_UsersRecommend( año : int ):
    ''' Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''
    
    # Cargo los DataFrames.
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    
    
    if año not in user_review['Año'].unique():
        return 'No se encuentra ningún registro con ese año. Pruebe otro.'
    

    # Filtro por año.
    review_filtered = user_review.loc[user_review['Año'] == año]
    
    
    # Filtro por reviews positivas.
    review_positivas = review_filtered[review_filtered['sentiment_analysis'] == 2].reset_index()
    
    
    # Encuentro los valores más altos
    conteo = review_positivas.groupby('item_id')['sentiment_analysis'].sum().nlargest(3).reset_index()
    
    
    # Consigo los nombres de los juegos con merge
    conteo = pd.merge(conteo,steam_games[['id','app_name']],left_on='item_id', right_on='id', how='outer')

    # Creo el diccionario
    dic = [{'Puesto 1' : conteo['app_name'][0]},
       {'Puesto 2' : conteo['app_name'][1]},
       {'Puesto 3' : conteo['app_name'][2]},]
    
    return dic



### Función 4 ###
def func_UsersWorstDeveloper( año : int ):
    '''
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''
    
    # Cargo los DataFrames.
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    
    
    if año not in user_review['Año'].unique():
        return 'No se encuentra ningún registro con ese año. Pruebe otro.'
    

    # Filtro por año.
    review_filtered = user_review.loc[user_review['Año'] == año]
    
    
    # Filtro por reviews negativas.
    review_negativas = review_filtered[review_filtered['sentiment_analysis'] == 0].reset_index()
    
    
    # Encuentro los valores más altos
    conteo = review_negativas.groupby('item_id')['sentiment_analysis'].sum().nlargest(3).reset_index()
    
    
    # Consigo los nombres de los juegos con merge
    conteo = pd.merge(conteo,steam_games[['id','app_name']],left_on='item_id', right_on='id', how='outer')

    # Creo el diccionario
    dic = [{'Puesto 1' : conteo['app_name'][0]},
       {'Puesto 2' : conteo['app_name'][1]},
       {'Puesto 3' : conteo['app_name'][2]},]
    
    return dic



### Función 5 ###
def sentiment(developer:str):
    '''
    Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}
    '''

    # Cargo los DataFrames.
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    

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