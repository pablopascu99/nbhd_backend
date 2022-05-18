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
    return {"Odio": odio/len(predicciones) * 100 , "No Odio":  no_odio/len(predicciones) * 100}

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurl = "https://www.20minutos.es/"

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurl_mundo = "https://ariadna.elmundo.es/"

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurlmunicipios = "https://noticiasparamunicipios.com/"

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
        res_20mins = resultados(pred)
        return res_20mins

# funcion aux 2: esta funcion filtra la página elmundo.com por localidad para obtener la url
def filtrar_localidad_mundo(base_url):
    localidad = php_param
    localidad_adaptada = localidad.replace(" ", "+")
    if localidad_adaptada: 
        url_filtrada = base_url + "buscador/archivo.html?q=" + localidad_adaptada + "&b_avanzada="
    return url_filtrada

# funcion 1: esta funcion obtiene las urls privadas de cada item, además se realiza la paginacion
def obtener_url_privadas_mundo(url):
    #print(url)
    hrefs = []
    puntero = True
    actual = url
    i = 1
    while(puntero):
        soup = BeautifulSoup(requests.get(actual, headers=headers).text, 'html.parser')
        lista_noticias = soup.find_all('h3')
        for noticia in lista_noticias:
            href = noticia.find('a')['href']
            hrefs.append(href)
        lis = soup.find_all('li')
        for li in lis:
            if li.text == "Siguiente »":
                elemento = li
        #nxt = soup.find(lambda tag:soup.name=="li" and "Siguiente" in tag.text)
        #siguiente = soup.find_all('li', string="Siguiente")
        if ((elemento) and len(hrefs) < 50):
            actual = re.sub('&b_avanzada=','&t=1&i=' + str(i) + '1&n=10&fd=0&td=0&w=70&s=1&no_acd=1', url)
            i = i + 1
        else:
            puntero = False
    #print(len(hrefs))
    #print(i)
    #print(hrefs)
    return hrefs


# funcion 2: esta funcion obtiene los datos de cada item de la página elmundo.com
def scrapear_noticia_mundo(url_privada):
    soupNoticia = BeautifulSoup(requests.get(url_privada, headers=headers).text, 'html.parser')
    premium = soupNoticia.find('div', {'class':'ue-c-article__premium-tag'})
    texto=""
    if premium is None:
        try:
            estructuraTexto = soupNoticia.find('div', {'class': 'ue-l-article__body ue-c-article__body'})
            if estructuraTexto is not None: 
                # Cogemos los p de la estructura de texto que conformaran todo el texto que necesitamos
                childrenTexto = estructuraTexto.findChildren("p" , recursive=False)
                for childTexto in childrenTexto:
                    texto = texto + childTexto.text
                    texto = re.sub('#',' ', texto)
        except: 
            texto = 'No texto'
    return texto

# esta funcion obtiene una lista con los datos de todas las noticias de la página elmundo.com
def scraper_elmundo(url):
    modelo = joblib.load('../resources/py/modelo.bin') #../resources/py/
    url_filtrada = filtrar_localidad_mundo(url)
    response = requests.get(url_filtrada)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        lista_urls = obtener_url_privadas_mundo(url_filtrada)
        collecion = []
        for href in lista_urls:
            texto = scrapear_noticia_mundo(href)
            tokens = tokenizar_texto(texto)
            palabras = limpiar_texto(tokens)
            texto_limpio = stemming(palabras)
            collecion.append(texto_limpio)
        pred = predecir_clases(modelo, collecion)
        res_mundo = resultados(pred)
        return res_mundo

# funcion aux 1: esta funcion filtra la página noticiasparamunicipios.com por localidad para obtener la url
def filtrar_localidad_municipios(base_url):
    localidad = php_param
    localidad_adaptada = localidad.replace(" ", "+")
    if localidad_adaptada: 
        url_filtrada = base_url + "?s=" + localidad_adaptada
    return url_filtrada

# funcion 1: esta funcion obtiene las urls privadas de cada item, además se realiza la paginacion
def obtener_url_privadas_municipios(url):
    #print(url)
    hrefs = []
    puntero = True
    actual = url
    i = 2
    while(puntero):
        soup = BeautifulSoup(requests.get(actual, headers=headers).text, 'html.parser')
        lista_noticias = soup.find_all('h2', class_='entry-title')
        for noticia in lista_noticias:
            href = noticia.find('a')['href']
            hrefs.append(href)
        if (soup.find('svg', class_='svg-icon') and i < 2):
            actual = re.sub('https://noticiasparamunicipios.com/','https://noticiasparamunicipios.com/page/' + str(i) + '/', url)
            i = i + 1
        else:
            puntero = False
    #print(len(hrefs))
    #print(hrefs)
    return hrefs

# funcion 2: esta funcion obtiene los datos de cada item de la página noticiasparamunicipios.com
def scrapear_noticia_municipios(url_privada):
    soupNoticia = BeautifulSoup(requests.get(url_privada, headers=headers).text, 'html.parser')
    content = soupNoticia.find('div', {'class':'entry-content'})
    try:
        texto = " ".join([p.text for p in content.find_all('p')])
    except: 
        texto = 'No texto'
    return texto

# esta funcion obtiene una lista con los datos de todas las noticias de la página noticiasmunicipiosmadrid.com
def scraper_noticasmunipiosmadrid(url):
    modelo = joblib.load('../resources/py/modelo.bin') #../resources/py/
    url_filtrada = filtrar_localidad_municipios(url)
    response = requests.get(url_filtrada)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        lista_urls = obtener_url_privadas_municipios(url_filtrada)
        collecion = []
        for href in lista_urls:
            texto = scrapear_noticia_municipios(href)
            tokens = tokenizar_texto(texto)
            palabras = limpiar_texto(tokens)
            texto_limpio = stemming(palabras)
            collecion.append(texto_limpio)
        pred = predecir_clases(modelo, collecion)
        res = resultados(pred)
        return res

def calcular_media(lista_dicc):
    total_odio = 0.0
    total_no_odio = 0.0
    for dicc in lista_dicc:
        total_odio += dicc["Odio"]
        total_no_odio += dicc["No Odio"]
    media_odio = total_odio / len(lista_dicc)
    media_no_odio = total_no_odio / len(lista_dicc)
    return {'media_odio': media_odio, 'media_no_odio': media_no_odio}

dicc1 = scraper_elmundo(baseurl_mundo) 
#dicc2 = scraper_20minutos(baseurl)
#dicc3 = scraper_noticasmunipiosmadrid(baseurl)

lista_pred_scrapers = []
lista_pred_scrapers.append(dicc1)
#lista_pred_scrapers.append(dicc2)
#lista_pred_scrapers.append(dicc3)

print(calcular_media(lista_pred_scrapers))

