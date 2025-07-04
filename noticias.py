import requests, math
with open('stopwords-es.txt', 'r', encoding='utf-8') as archivo:
    pirrelevante = [linea.strip() for linea in archivo]
'''
Esta función utiliza el servicio newsapi para obtener una lista de noticias.
La función obtiene solo las noticias para Uruguay y las devuelve en una lista
Cada noticia contiene los primeros 200 caracters de la noticia completa.
'''
def get_news(apikey, query):
    # Parámetros de consulta
    params = {'q': query,'apiKey': apikey, "language":"e" "s"}
    response = requests.get("https://newsapi.org/v2/everything", params=params)
    # Obtiene los artículos del json
    articles = response.json()['articles']
    news = []
    # Toma la descripción de cada noticia
    for article in articles:
        news.append(article['description'])
    return news

def normalizar(string: str): #Declara la función normalizar, que toma un argumento string
    reemplazos = { #reemplazos es un dict qué contiene cada vocal con tílde y su correspondiente sin tílde, para faclitar el remplazar estas letras
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
    }
    string = string.lower() #Convierte todo el string a minúsculas
    stringNormalizado = '' #String vacío donde se va a almacenar el resultado (el string normalizado)
    for s in string: #Recorre cada letra del string
        if s.isalpha() or s == ' ': #Esta función toma cada letra del string y chequea que sea un caractér alfabético y que tenga por lo menos un caractér
            if s in ['á', 'é', 'í', 'ó', 'ú']: #Revisa si la letra es una vocal con tílde
                stringNormalizado += reemplazos[s] #Si la letra es una vocal con tílde, elimina el tílde y agrega a stringNormalizado su correspondiente sin tílde utilizando el dict reemplazos
            else:
                stringNormalizado += s #Si la letra no es una vocal con tílde, solamente agrega esta letra a stringNormalizado

    return stringNormalizado #Devuelve el string

def getTF(noticia, termino):
    noticia = normalizar(noticia).split(' ')
    for i in noticia:
        if i in pirrelevante:
            noticia.remove(i)
    return noticia.count(termino) / len(noticia)

def allTFs(noticias):
    tfs = []
    for noticia in noticias:
        tf = {}        
        for palabra in noticia.split(' '):
            tf[palabra] = getTF(noticia, palabra)
        tfs.append(tf)

def getIDFs(noticias):
    todasLasPalabras = []
    for noticia in noticias:
        for palabra in noticia.split(' '):
            todasLasPalabras.append(palabra)   

    idf = {}
    for palabra in set(todasLasPalabras):
        idf[palabra] = math.log((len(noticias) / len(set([n for n in noticias if palabra in n.split(' ')]))), math.e)

    return idf

def puntuaciones(noticias):
    idf = getIDFs(noticias)
    puntos = {}
    for noticia in noticias:
        puntuacionNoticia = {}
        for palabra in noticia.split(' '):
            puntuacionNoticia[palabra] = getTF(noticia, palabra) * idf[palabra]
        puntos[noticia] = puntuacionNoticia

    return puntos

def buscar():
    busqueda = input('Busqueda: ')
    query = normalizar(busqueda)
    news = get_news("89da03c33cb240e7bcc79df0b4068416", query)
    noticias = [normalizar(n) for n in news]
    puntos = puntuaciones(noticias)

    maxPuntos = float('-Infinity')
    for noticia in puntos.keys():
        puntosPorDict = 0
        for palabra in query.split(' '):
            if palabra in puntos[noticia]:
                puntosPorDict += puntos[noticia][palabra]
        if puntosPorDict > maxPuntos:
            maxNoticia = noticia
            maxPuntos = puntosPorDict

    print(f'La noticia \033[34m\"{maxNoticia}\"\033[0m es el mejor resultado para la busqueda \033[33m\"{busqueda}\"\033[0m')
    return maxNoticia

buscar()
