def realizar_operaciones(numero):
    binario = bin(numero).replace("0b", "")
    octal = oct(numero)[2:]
    hexadecimal = hex(numero)[2:]
    return binario, octal, hexadecimal

# Solicitar el número al usuario
num = int(input("Ingresa un número: "))

# Llamar a la función y obtener las conversiones
binario, octal, hexadecimal = realizar_operaciones(num)

# Mostrar los resultados
print(f"""
Resultados:
- Binario: {binario}
- Octal: {octal}
- Hexadecimal: {hexadecimal}
""")
