import re
import requests
from bs4 import BeautifulSoup
import sys

php_param = sys.argv[1]
php_param_2 = sys.argv[2]

# direccion base del scraper
# a esta dirección se le aplicaran diferentes filtros y formatos segun las opciones del usuario
baseurl = "https://www.yaencontre.com"

# declaramos los headers para la petición
headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}

# funcion aux 1 : esta función transforma la localidad (en formato ingresado) a formato url de la página yaencontre.com
# ejemplo: las rozas de madrid -> rozas-de-madrid-las
def transformar_localidad_url(cadena):
    cadena_final = ""
    if re.match(r'\blas ', cadena):
        las_cadena = re.sub(r'\blas ','', cadena)
        cadena_final = las_cadena + " las"
    elif re.match(r'\bel ', cadena):
        el_cadena = re.sub(r'\bel ', '', cadena)
        cadena_final = el_cadena + " el"
    elif re.match(r'\bla ', cadena):
        la_cadena = re.sub(r'\bla ', '', cadena)
        cadena_final = la_cadena + " la"
    elif re.match(r'\blos ', cadena):
        los_cadena = re.sub(r'\blos ', '', cadena)
        cadena_final = los_cadena + " los"
    else:
        cadena_final = cadena
    cadena_url = re.sub(r' ', '-', cadena_final)
    return cadena_url

# funcion aux 2: esta funcion filtra la página yaencontre.com por localidad y tipo de inmueble para obtener la url
def filtrar_inmuebles(baseurl):
    #print("Tipo de inmueble\n 1. Edificios \n 2. Negocios \n 3. Pisos \n 4. Garajes \n 5. Casas \n 6. Terrenos \n 7. Naves \n 8. Oficinas \n 9. Locales \n#########################")
    #op = int(input("Elige que inmueble necesita: "))
    #localidad = input("Elige la localidad: ")
    # a la hora de ingresar la localidad recomendamos echar un vistazo antes a si existe en yaencontre, ya que puede tener un formato determinado.
    localidad_transformada = transformar_localidad_url(php_param)
    if int(php_param_2) == 1:
        url_filtrada = baseurl + '/venta/edificios/' + localidad_transformada
    elif int(php_param_2) == 2:
        url_filtrada = baseurl + '/venta/negocios/' + localidad_transformada
    elif int(php_param_2) == 3:
        url_filtrada = baseurl + '/venta/pisos/' + localidad_transformada
    elif int(php_param_2) == 4:
        url_filtrada = baseurl + '/venta/garajes/' + localidad_transformada
    elif int(php_param_2) == 5:
        url_filtrada = baseurl + '/venta/casas/' + localidad_transformada
    elif int(php_param_2) == 6:
        url_filtrada = baseurl + '/venta/terrenos/' + localidad_transformada
    elif int(php_param_2) == 7:
        url_filtrada = baseurl + '/venta/naves/' + localidad_transformada
    elif int(php_param_2) == 8:
        url_filtrada = baseurl + '/venta/oficinas/' + localidad_transformada
    elif int(php_param_2) == 9:
        url_filtrada = baseurl + '/venta/locales/' + localidad_transformada
    return url_filtrada

# funcion 1: esta funcion obtiene las urls privadas de cada inmueble, además se realiza la paginacion
def obtener_url_privadas(url):
    #print(url)
    hrefs = []
    puntero = True
    actual = url
    i = 2
    while (puntero):
        soup = BeautifulSoup(requests.get(actual, headers=headers).text, 'html.parser')
        lista_inmuebles = soup.find_all('article', class_='ThinPropertyList property-info pointer pos-rel')
        for inmueble in lista_inmuebles:
            h2 = inmueble.find('h2', class_='title d-ellipsis logo-aside')
            href = h2.find('a')['href']
            hrefs.append(baseurl + href)
        if soup.find('button',class_='button next-button'):
            actual = url + "/pag-" + str(i)
            i = i + 1
        else:
            puntero = False
    #print(len(hrefs))
    #print(hrefs)
    return hrefs

# funcion 2: esta funcion obtiene los datos de un inmueble de la página yaencontre.com tras haber obtenido la url de dicho inmueble privada
def scrapear_inmueble(url_privada):
    soup = BeautifulSoup(requests.get(url_privada, headers=headers).text, 'html.parser')
    try:
        precio = soup.find('span', class_='d-block price').text.strip()
    except:
        precio = "No precio"   
    try: 
        nombre = soup.find('h1', id='title-realestate').text
    except:
        nombre = "No nombre"
    imagenes = []
    for imagen in soup.find_all('source', attrs = {'srcset' : True}):
        imagenes.append(imagen['srcset'])
    try:
        descripcion = soup.find('div', class_='raw-format l-height-lg').text
        descripcion = re.sub(r'\"','', descripcion)
        descripcion = re.sub(r'\'','', descripcion)
    except:
        descripcion = "No descripcion"
    try:
        habitaciones = soup.find('div', class_='icon-room').next_element.text
    except:
        habitaciones = "No habitaciones"
    try:
        banos = soup.find('div', class_='icon-bath').next_element.text
    except:
        banos = "No banos"
    try:
        metros2 = soup.find('div', class_='icon-meter').next_element.text
    except:
        metros2 = "No metros2"
    try:
        telefono = soup.find('a', class_='button call btn icon-phone-2').next_element.text
    except:
        telefono = "No telefono"
    try:
        ubicacionesRaw = soup.find("script",type="application/ld+json").text
        ubicacionesGroup = re.search(r"GeoCoordinates\",\"latitude\":(.*?),\"longitude\":(.*?)}", ubicacionesRaw)
        ubicaciones = []
        ubicaciones.append(ubicacionesGroup.group(1))
        ubicaciones.append(ubicacionesGroup.group(2))
    except:
        ubicaciones = "no ubicacion"
    try:
        caracteristicas = []
        for caracteristica in soup.find_all('div', class_='extrasItem'):
            caracteristicas.append(caracteristica.text)
    except:
        caracteristicas = "No caracteristicas"
    datos_inmueble = {
        'nombre': nombre,
        'precio': precio,
        'imagenes': imagenes,
        'descripcion': descripcion,
        'enlace': url_privada,
        'habitaciones': habitaciones,
        'banos': banos,
        'metros2': metros2,
        'telefono': telefono,
        'ubicacion': ubicaciones,
        'caracteristicas': caracteristicas
    }
    #print(datos_inmueble)
    return datos_inmueble

# esta funcion obtiene una lista con los datos de todos los inmuebles de la página yaencontre.com tras haber obtenido la url de dicho inmueble
# unifica todo lo anterior en una sola función  
def scraper_yaencontre(url):
    url_filtrada = filtrar_inmuebles(url)
    response = requests.get(url_filtrada)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        #print("Pagina encontrada")
        lista_urls = obtener_url_privadas(url_filtrada)
        lista_datos = []
        for href in lista_urls:
            datos = scrapear_inmueble(href)
            lista_datos.append(datos)
            #print(datos)
        #print(lista_datos)
        #print("Inmuebles obtenidos")
    # output: lista de diccionarios por cada inmueble: [{datos inmueble 1},{datos inmueble 2}]
    return lista_datos

# llamamos a la función principal
print(scraper_yaencontre(baseurl))