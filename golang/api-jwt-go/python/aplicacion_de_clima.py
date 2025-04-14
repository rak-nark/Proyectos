import requests

API_KEY = '005c738e0ef9f2373e3d606384c3cb49'
API_URL = "http://api.openweathermap.org/data/2.5/weather"

def obtener_clima(ciudad):
    try:
        params = {
            'q': ciudad,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        respuesta = requests.get(API_URL, params=params)
        datos = respuesta.json()

        if respuesta.status_code != 200:
            raise ValueError(f"Error en la API: {datos.get('message', 'Error desconocido')}")
        
        clima = {
            'ciudad': datos['name'],
            'temperatura': datos['main']['temp'],
            'descripcion': datos['weather'][0]['description'],
            'humedad': datos['main']['humidity'],
            'viento': datos['wind']['speed'],
            'presion': datos['main']['pressure'],
        }

        return clima
    except Exception as e:
        print(f"Error al obtener clima: {e}")
        return None

def mostrar_clima(ciudad):
    clima = obtener_clima(ciudad)
    if clima:
        print(f"Clima en {clima['ciudad']}:")
        print(f"Temperatura: {clima['temperatura']}°C")
        print(f"Descripción: {clima['descripcion']}")
        print(f"Humedad: {clima['humedad']}%")
        print(f"Velocidad del viento: {clima['viento']} m/s")
        print(f"Presión atmosférica: {clima['presion']} hPa")
    else:
        print("No se pudo obtener el clima")

if __name__ == "__main__":
    ciudad = input("Ingrese el nombre de la ciudad: ")
    mostrar_clima(ciudad)
