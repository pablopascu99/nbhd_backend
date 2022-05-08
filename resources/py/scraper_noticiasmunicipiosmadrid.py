import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

php_param = sys.argv[1]

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurl = "https://noticiasparamunicipios.com/"

# declaramos los headers para la petición
headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}

# funcion aux 1: esta funcion filtra la página noticiasparamunicipios.com por localidad para obtener la url
def filtrar_localidad(base_url):
    localidad = php_param
    localidad_adaptada = localidad.replace(" ", "+")
    if localidad_adaptada: 
        url_filtrada = base_url + "?s=" + localidad_adaptada
    return url_filtrada



# funcion 1: esta funcion obtiene las urls privadas de cada item, además se realiza la paginacion
def obtener_url_privadas(url):
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
def scrapear_noticia(url_privada):
    soupNoticia = BeautifulSoup(requests.get(url_privada, headers=headers).text, 'html.parser')
    content = soupNoticia.find('div', {'class':'entry-content'})
    try:
        titulo = soupNoticia.find('h1', {'class':'entry-title'}).text
    except: 
        titulo = 'No titulo'
    try:
        texto = " ".join([p.text for p in content.find_all('p')])
    except: 
        texto = 'No texto'
    datos_noticia = {
        'titulo': titulo,
        'texto': texto
    }
    return datos_noticia

# esta funcion obtiene una lista con los datos de todas las noticias de la página 20minutos.com
def scraper_noticasmunipiosmadrid(url):
    url_filtrada = filtrar_localidad(url)
    response = requests.get(url_filtrada)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        print("Pagina encontrada")
        lista_urls = obtener_url_privadas(url_filtrada)
        lista_datos = []
        for href in lista_urls:
            datos = scrapear_noticia(href)
            lista_datos.append(datos)
            #print(datos)
        #print(lista_datos)
        print("Noticias obtenidas")
    # output: lista de diccionarios por cada noticia: [{datos noticia 1},{datos noticia 2}]
    return lista_datos

#print(filtrar_localidad(baseurl))
#obtener_url_privadas(baseurl)
print(scraper_noticasmunipiosmadrid(baseurl))
# si devuleve un [] es que no hay ningun item dado esa localidad y filtro


