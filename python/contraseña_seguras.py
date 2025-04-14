import string
import random

# Validar que el tamaño de la contraseña sea un entero positivo
while True:
    try:
        longitud = int(input("Ingrese el tamaño de la contraseña: "))
        if longitud <= 0:
            raise ValueError("El tamaño debe ser mayor que 0.")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}. Inténtelo de nuevo.")

# Crear el conjunto de caracteres
caracteres = string.ascii_letters + string.digits + string.punctuation

# Generar la contraseña
contraseña = "".join(random.choice(caracteres) for _ in range(longitud))

# Imprimir la contraseña generada
print(f"La contraseña generada es: {contraseña}")
