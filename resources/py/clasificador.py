import re
import requests
from bs4 import BeautifulSoup
import sys
import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SpanishStemmer
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

php_param = sys.argv[1]

def tokenizar_texto(texto: str):
    lista_tokens = word_tokenize(texto.lower(), language="spanish")
    return lista_tokens


def limpiar_texto(lista_tokens: list):
    palabras = []
    fichero_parada = open("../resources/py/Lista_Stop_Words.txt", "r", encoding="utf8")
    lista_parada = fichero_parada.read().split("\n")
    puntuacion = list(string.punctuation)
    lista_parada += puntuacion
    for palabra in lista_tokens:
        if palabra not in lista_parada:
            palabras.append(palabra)
    return palabras

def stemming(lista_palabras: list):
    texto = ""
    stemmer = SpanishStemmer()
    for palabra in lista_palabras:
        s = stemmer.stem(palabra)
        texto = texto + " " + s
    return texto

def predecir_clases(modelo, coleccion_noticias: list):
    tf = TfidfVectorizer(vocabulary=joblib.load('../resources/py/vocabulario.bin'))
    vectores_noticias = tf.fit_transform(coleccion_noticias).toarray()
    matriz_idf = pd.DataFrame(vectores_noticias, columns=tf.get_feature_names_out())
    predicciones = modelo.predict(matriz_idf)
    return predicciones

def resultados(predicciones: list):
    odio = 0
    no_odio = 0
    for pred in predicciones:
        if pred == 'Odio':
            odio += 1
        else:
            no_odio += 1
    return {"Odio": odio/len(predicciones) * 100, "No Odio": no_odio/len(predicciones) * 100}

# php_param = sys.argv[1]

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurl = "https://www.20minutos.es/"

# declaramos los headers para la petición
headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}
# funcion aux 2: esta funcion filtra la página 20minutos.com por localidad para obtener la url
def filtrar_localidad(base_url):
    localidad = php_param
    localidad_adaptada = localidad.replace(" ", "+")
    if localidad_adaptada: 
        url_filtrada = base_url + "busqueda/?q=" + localidad_adaptada + "&sort_field=&category=&publishedAt%5Bfrom%5D=&publishedAt%5Buntil%5D="
    return url_filtrada

# funcion 1: esta funcion obtiene las urls privadas de cada item, además se realiza la paginacion
def obtener_url_privadas(url):
    hrefs = []
    puntero = True
    actual = url
    i = 2
    while(puntero):
        soup = BeautifulSoup(requests.get(actual, headers=headers).text, 'html.parser')
        lista_noticias = soup.find_all('article', class_='media')
        for noticia in lista_noticias:
            h1 = noticia.find('h1')
            href = h1.find('a')['href']
            hrefs.append(href)
        if (soup.find('li', class_='last') and i < 5):
            actual = re.sub('busqueda/','busqueda/' + str(i) + '/', url)
            i = i + 1
        else:
            puntero = False
    return hrefs

# funcion 2: esta funcion obtiene los datos de cada item de la página 20minutos.com
def scrapear_noticia(url_privada):
    soupNoticia = BeautifulSoup(requests.get(url_privada, headers=headers).text, 'html.parser')
    try:
        texto = soupNoticia.find('div', {'class':'article-text'}).text
    except: 
        texto = 'No texto'
    return texto

# esta funcion obtiene una lista con los datos de todas las noticias de la página 20minutos.com
def scraper_20minutos(url):
    modelo = joblib.load('../resources/py/modelo.bin')
    url_filtrada = filtrar_localidad(url)
    response = requests.get(url_filtrada)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        lista_urls = obtener_url_privadas(url_filtrada)
        collecion = []
        for href in lista_urls:
            texto = scrapear_noticia(href)
            tokens = tokenizar_texto(texto)
            palabras = limpiar_texto(tokens)
            texto_limpio = stemming(palabras)
            collecion.append(texto_limpio)
        pred = predecir_clases(modelo, collecion)
        res = resultados(pred)
        return res

    # output: lista de diccionarios por cada noticia: [{datos noticia 1},{datos noticia 2}]

#print(filtrar_localidad(baseurl))
#obtener_url_privadas(baseurl)
print(scraper_20minutos(baseurl))
# si devuleve un [] es que no hay ningun item dado esa localidad y filtro