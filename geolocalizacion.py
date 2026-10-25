import requests
import urllib.parse

# Configuración de URLs y parámetros base de Graphhopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
idioma = "es"

# Reemplaza la siguiente cadena con tu API Key real de Graphhopper
key = "f9d10936-4f69-476d-9235-04b8f65ffd25"

def geocoding(location, key):
    # Validación de entrada vacía
    while location == "":
        location = input("Por favor, ingrese una ubicación válida: ")
    
    # Construcción de parámetros codificados para la URL de geocodificación
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key, "locale": idioma})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if len(state) != 0 and len(country) != 0:
            new_loc = f"{name}, {state}, {country}"
        elif len(state) != 0:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        
        print(f"URL de Geocodificación para {new_loc} (Tipo de Ubicación: {value}):\n{url}\n")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print(f"Estado API de Geocodificación: {json_status}\nMensaje de error: {json_data.get('message', 'Ubicación no encontrada')}")
            
    return json_status, lat, lng, new_loc


# Bucle principal de interacción con el usuario
while True:
    print("="*55)
    print("SISTEMA DE PLANIFICACIÓN DE VIAJES DE NAVEGACIÓN")
    print("Escriba 's' o 'salir' en cualquier momento para terminar.")
    print("="*55)
    
    loc1 = input("Ingrese la ubicación de origen: ")
    if loc1.lower() in ["salir", "s", "quit", "q"]:
        print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
        break
        
    orig = geocoding(loc1, key)
    if orig[0] != 200:
        continue

    loc2 = input("Ingrese la ubicación de destino: ")
    if loc2.lower() in ["salir", "s", "quit", "q"]:
        print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
        break
        
    dest = geocoding(loc2, key)
    if dest[0] != 200:
        continue
    
    print("="*55)
    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "locale": idioma, "vehicle": "car"}) + op + dp
        
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()
        
        print(f"Estado de la API de Rutas: {paths_status}\nURL de la API de Rutas:\n{paths_url}")
        print("="*55)
        print(f"Indicaciones de viaje desde '{orig[3]}' hasta '{dest[3]}'")
        print("="*55)
        
        if paths_status == 200:
            # Conversión de distancia y tiempo
            distancia_m = paths_data["paths"][0]["distance"]
            tiempo_ms = paths_data["paths"][0]["time"]
            
            millas = distancia_m / 1000 / 1.61
            km = distancia_m / 1000
            
            seg = int(tiempo_ms / 1000 % 60)
            minu = int(tiempo_ms / 1000 / 60 % 60)
            hrs = int(tiempo_ms / 1000 / 60 / 60)
            
            # Salida con máximo dos decimales
            print(f"Distancia Recorrida: {millas:.2f} millas / {km:.2f} km")
            print(f"Duración del Viaje: {hrs:02d}:{minu:02d}:{seg:02d}")
            print("="*55)
            print("NARRATIVA DEL VIAJE (INSTRUCCIONES PASO A PASO):")
            print("="*55)
            
            # Recorrido iterativo de instrucciones paso a paso
            for inst in paths_data["paths"][0]["instructions"]:
                paso = inst["text"]
                dist_paso = inst["distance"]
                print(f"• {paso} ({dist_paso/1000:.2f} km / {dist_paso/1000/1.61:.2f} millas)")
                
            print("="*55 + "\n")
        else:
            print(f"Mensaje de error: {paths_data.get('message', 'No se pudo calcular la ruta')}")
            print("*"*55 + "\n")
