import requests

# Reemplaza 'TU_API_KEY' con tu clave de API real de ExchangeRate-API
API_URL = "https://v6.exchangerate-api.com/v6/ace7fbb6695dcf748eb04e23/latest"

def obtener_tasas(base):
    """Obtiene las tasas de cambio para la moneda base."""
    try:
        # Solicitud a la API con la moneda base y la clave de acceso
        respuesta = requests.get(f"{API_URL}/{base}")
        datos = respuesta.json()

        # Verifica el estado de la respuesta
        if respuesta.status_code != 200 or 'conversion_rates' not in datos:
            raise ValueError(f"Error en la API: {datos.get('error-type', 'Error desconocido')}")

        return datos['conversion_rates']
    except Exception as e:
        print(f"Error al obtener tasas: {e}")
        return None

def convertir_monedas(cantidad, tasa_origen, tasa_destino):
    """Convierte una cantidad según las tasas de origen y destino."""
    return cantidad * (tasa_destino / tasa_origen)

def conversor_monedas():
    """Función principal para realizar la conversión de monedas."""
    print("=== Conversor de Monedas ===")

    base = input("Ingrese la moneda base (por ejemplo, USD): ").upper()
    tasas = obtener_tasas(base)

    if not tasas:
        print("No se pudo obtener las tasas de cambio. Intente más tarde.")
        return

    print("Monedas disponibles: ", ", ".join(tasas.keys()))

    destino = input("Ingrese la moneda a la que desea convertir (por ejemplo, EUR): ").upper()
    if destino not in tasas:
        print("Moneda no válida.")
        return

    try:
        cantidad = float(input(f"Ingrese la cantidad en {base}: "))
        resultado = convertir_monedas(cantidad, tasas[base], tasas[destino])
        print(f"{cantidad:.2f} {base} equivale a {resultado:.2f} {destino}.")
    except ValueError:
        print("Cantidad inválida. Inténtelo de nuevo.")

if __name__ == "__main__":
    conversor_monedas()


