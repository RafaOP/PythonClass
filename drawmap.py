import requests
import folium
import polyline
import math

import numpy as np

#858585 instead of blue for asphalt
# In this order: gray, light brown, dark brown, orange, bright orange, dark red
TERRAIN_COLOR = ['blue', '#877965', '#5e4e36', '#b36b00', '#ff9800', '#850000']

# Graphhopper
GRAPHHOPPER_ROUTE = 'https://graphhopper.com/api/1/route'
# Rafa
GRAPHHOPPER_API_KEY = 'f9e77954-a5fd-416e-8087-1c1c456c6fc8'

def desenhaMapa(coords, caminho):
    m = folium.Map(start=coords[0], zoom_start=13)

    for coord in coords:
        folium.Marker(coord, icon=folium.Icon(icon='home', color='blue', prefix='fa')).add_to(m)

    locations = polyline.decode(caminho)
    folium.PolyLine(locations).add_to(m)

    m.save('map.html')

def achaCEP(estado, cidade, rua):
    resposta = requests.get('http://viacep.com.br/ws/' + estado + '/' + cidade + '/' + rua + '/json/')
    resposta = resposta.json()

    return resposta[0]['cep']

def achaCoord(endereco):
    locale = 'br'
    url = 'https://graphhopper.com/api/1/geocode?q=' + endereco + '&locale=' + locale + '&debug=true&key=' + GRAPHHOPPER_API_KEY
    print (url)
    exit()
    resposta = requests.get(url)
    resposta = resposta.json()

    return (resposta['hits'][0]['point']['lat'], resposta['hits'][0]['point']['lng'])

def achaCaminho(a, b):
    coords = 'point=' + str(a[0]) + ',' + str(a[1]) + '&point=' + str(b[0]) + ',' + str(b[1])
    params = 'instructions=false&points_encoded=true&type=json&debug=true'
    route = requests.get(GRAPHHOPPER_ROUTE + '?' + coords + '&' + params + '&key=' + GRAPHHOPPER_API_KEY)
    route = route.json()

    return route['paths'][0]['points']

def main():
    estado = 'MG'
    cidade = 'Viçosa'
    rua = 'Avenida Bueno Brandão'

    univicosa = (-20.728718, -42.865061)
    # estado = input ('Estado: ')
    # cidade = input ('Cidade: ')
    # rua = input ('Rua: ')

    cep = achaCEP(estado, cidade, rua)
    print (cep)

    casa = achaCoord(rua + ', ' + cidade + ' - ' + estado)
    print (casa)

    caminho = achaCaminho(casa, univicosa)
    # print (caminho)
    # exit()

    desenhaMapa([casa, univicosa], caminho)


if __name__ == '__main__':
    main()