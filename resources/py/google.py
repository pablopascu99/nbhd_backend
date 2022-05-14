import googlemaps
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

##############################################################################
####   NO USAR MUCHO QUE ES API DE GOOGLE Y SE NOS ACABAN LOS CREDITOS   #####
##############################################################################

map_client = googlemaps.Client(key='AIzaSyDoutziQhNdTUmPALX9D7UO1VUflx4ZI9Q')
places = map_client.places_nearby(location=(40.460743, -3.459096), radius=50)

#print(places)
listaLugares = []
lugares = []
for item in places['results']:
    if item['types'][0]!='route': 
        lugar_id = map_client.place(item['place_id'])
        lugares.append(lugar_id)
for lugar in lugares:
    lat = lugar['result']['geometry']['location']['lat']
    lng = lugar['result']['geometry']['location']['lng']
    nombre = lugar['result']['name']
    direccion = lugar['result']['formatted_address'] #Puede que no tenga alguno(revisar)
    try:
        telefono = lugar['result']['formatted_phone_number']
    except:
        telefono = "No hay telefono"
    tipo_establecimiento = lugar['result']['types']
    try:
        puntuacion_media = lugar['result']['rating']
    except:
        puntuacion_media = "Sin puntuacion media"
    textReviews=[]
    media_analisis=0
    cont=0
    try:
        reviews_text = lugar['result']['reviews']
        for item in reviews_text:
            # text= GoogleTranslator(source='english', target='spanish').translate(item['text'])
            # textReviews.append(text)
            textReviews.append(item['text'])
            vs = SentimentIntensityAnalyzer()
            vs_result = vs.polarity_scores(item['text'])['compound']
            media_analisis = media_analisis + vs_result
            cont=cont+1
        media_analisis = media_analisis/cont
    except:
        texto = 'Not reviews'
        # texto = GoogleTranslator(source='english', target='spanish').translate(texto)
        textReviews.append(texto)
    place = {
        'nombre': nombre,
        'direccion': direccion,
        'latitud': lat,
        'longitud': lng,
        'tipo_establecimiento': tipo_establecimiento,
        'telefono': telefono,
        'puntuacion_media': puntuacion_media,
        'media_analisis': media_analisis,
        'reviews': textReviews,
    }
    listaLugares.append(place)
print(listaLugares)
# items = []
# textReviews=[]
# for item in places['results']:
#     items.append(item['place_id'])
# for place_id in items:
#     place = map_client.place(place_id)
#     textReview=[]
#     try:
#         reviews_text = place['result']['reviews']
#         for item in reviews_text:
#             text= GoogleTranslator(source='english', target='spanish').translate(item['text'])
#             textReview.append(text)
#         textReviews.append(textReview)
#     except:
#         texto = 'Not reviews'
#         text = GoogleTranslator(source='english', target='spanish').translate(texto)
#         textReview.append(text)
#         textReviews.append(textReview)
# print(textReviews)