import urllib.parse
import requests

graphhopper_api = "https://graphhopper.com/api/1/route?"
graphhopper_key = "78c74120-7f75-4152-9534-b9de231521a8"
nominatim_api = "https://nominatim.openstreetmap.org/search?"

def get_coordinates(location):
    params = {
        'q': location,
        'format': 'json'
    }
    url = nominatim_api + urllib.parse.urlencode(params)
    response = requests.get(url).json()
    if response:
        return response[0]['lat'], response[0]['lon']
    else:
        return None

def format_duration(milliseconds):
    seconds = int(milliseconds / 1000)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours} horas, {minutes} minutos, {seconds} segundos"

while True:
    orig = input("Ubicación inicial: ")
    if orig.lower() in ["salir", "s"]:
        break
    dest = input("Destino: ")
    if dest.lower() in ["salir", "s"]:
        break

    orig_coords = get_coordinates(orig)
    dest_coords = get_coordinates(dest)

    if not orig_coords or not dest_coords:
        print("No se pudieron encontrar coordenadas para las ubicaciones proporcionadas.")
        continue

    # Construir la URL con las coordenadas
    params = {
        "key": graphhopper_key,
        "point": [f"{orig_coords[0]},{orig_coords[1]}", f"{dest_coords[0]},{dest_coords[1]}"],
        "vehicle": "car",
        "locale": "es",
        "instructions": "true"
    }

    url = graphhopper_api + urllib.parse.urlencode(params, doseq=True)
    print("URL: " + url)

    # Realizar la solicitud GET y obtener los datos en formato JSON
    response = requests.get(url)
    json_data = response.json()

    if "message" in json_data:
        print("Error: " + json_data["message"])
    else:
        print("API Status: Successful request.\n")
        print("--------------------------------------------------")
        print("Directions from " + orig + " to " + dest)
        print("--------------------------------------------------")

        duration = format_duration(json_data["paths"][0]["time"])
        distance_km = json_data["paths"][0]["distance"] / 1000
        fuel_used_liters = (distance_km / 10) * 8  # Suponiendo un consumo de 8 litros cada 100 km

        print(f"Duracion del Viaje: {duration}")
        print(f"Kilometros: {distance_km:.2f} km")
        print(f"Bencina Gastada (Ltr): {fuel_used_liters:.2f} L")
        print("--------------------------------------------------")

        for each in json_data["paths"][0]["instructions"]:
            print(f"{each['text']} ({each['distance'] / 1000:.2f} km)")

        print("--------------------------------------------------\n")
