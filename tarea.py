import googlemaps
import json
from flask import Flask, jsonify, request

gmaps = googlemaps.Client(key='AIzaSyAAbZMe1pZtcETxTFcFIzXWykHRAY3xHOY')
flThing = Flask(__name__)

def getDirection(origin,destination):
    dir_res = gmaps.directions(origin, destination)
    direcciones = "{\n \"ruta\":[\n"

    for index in range(len(dir_res[0]['legs'][0]['steps'])):
        direcciones += "  {\n   \"lat\": "
        direcciones += str(dir_res[0]['legs'][0]['steps'][index]['start_location']['lat']) + ","
        direcciones += "\n   \"lon\": "
        direcciones += str(dir_res[0]['legs'][0]['steps'][index]['start_location']['lng'])
        
        if index == len(dir_res[0]['legs'][0]['steps']) - 1:
            direcciones += "\n  }\n"
        else:
            direcciones += "\n  },\n"
    
    direcciones += " ]\n}"
    print(direcciones)
    return direcciones

@flThing.route('/ejercicio1', methods = ['POST'])
def ejercicioUno():
    try:
        origin = request.json['origen']
        destination = request.json['destino']
    except:
        err={"Error": "Origen y/o Destino no encontrado(s)."}
        return jsonify(err), 400
    
    return getDirection(origin,destination)

def getRestaurants(origin):
    gresult = gmaps.geocode(origin)
    restau = gmaps.places_nearby((gresult[0]['geometry']['location']['lat'], gresult[0]['geometry']['location']['lng']), 40000, type = 'restaurant', keyword = 'restaurant')

    restaurantes = "{\n \"restaurantes\":[\n"

    for ind in range(len(restau['results'])):
        restaurantes += "  {\n    \"nombre\": \""
        temp = restau['results'][ind]['name'] 
        restaurantes += temp.encode('utf-8')
        restaurantes += "\",\n"
        restaurantes += "    \"lat\": "
        restaurantes += str(restau['results'][ind]['geometry']['location']['lat'])
        restaurantes += ",\n"
        restaurantes += "    \"lng\": "
        restaurantes += str(restau['results'][ind]['geometry']['location']['lng'])
        if ind == len(restau['results'])-1:
            restaurantes += "\n  }\n"
        else:
            restaurantes += "\n  },\n"
    
    restaurantes += " ]\n}"
    print(restaurantes)
    return restaurantes

@flThing.route('/ejercicio2', methods = ['POST'])
def ejercicioDos():
    try:
        origin = request.json['origen']
    except:
        err={"Error": "Punto de origen no encontrado."}
        return jsonify(err), 400
    
    return getRestaurants(origin)
    

if __name__ == '__main__':
    flThing.run(host = '0.0.0.0', port = 8080, debug = True)