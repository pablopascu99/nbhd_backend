import re
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurl = "https://www.20minutos.es/"

# declaramos los headers para la petición
headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}
# funcion aux 2: esta funcion filtra la página 20minutos.com por localidad para obtener la url
def filtrar_localidad(base_url):
    localidad = "alcobendas"
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
    url_filtrada = filtrar_localidad(url)
    response = requests.get(url_filtrada)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        lista_urls = obtener_url_privadas(url_filtrada)
        lista_datos = []
        for href in lista_urls:
            texto = scrapear_noticia(href)
            traductor = GoogleTranslator(target='en')
            if len(texto)>=5000:
                  texto = texto[0:4999]
            texto_traducido = traductor.translate(texto)
            vs = SentimentIntensityAnalyzer()
            vs_result = vs.polarity_scores(texto_traducido)
            lista_datos.append(vs_result)
        datos_noticia = {
              '20min': lista_datos,
        }
    # output: lista de diccionarios por cada noticia: [{datos noticia 1},{datos noticia 2}]
    return datos_noticia

#print(filtrar_localidad(baseurl))
#obtener_url_privadas(baseurl)
print(scraper_20minutos(baseurl))
# si devuleve un [] es que no hay ningun item dado esa localidad y filtro