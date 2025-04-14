import random

def generar_numeros_loteria(cantidad, minimo, maximo):
    """Genera una lista de números aleatorios únicos."""
    return random.sample(range(minimo, maximo + 1), cantidad)

def main():
    print("=== Simulador de Lotería ===")

    try:
        # Pedir los datos al usuario
        cantidad = int(input("¿Cuántos números desea generar? (por ejemplo, 6): "))
        minimo = int(input("¿Cuál es el número mínimo? (por ejemplo, 1): "))
        maximo = int(input("¿Cuál es el número máximo? (por ejemplo, 49): "))

        if cantidad > (maximo - minimo + 1):
            print("La cantidad de números no puede ser mayor al rango.")
            return
        
        # Generar los números de lotería
        numeros_ganadores = generar_numeros_loteria(cantidad, minimo, maximo)
        print(f"Los números ganadores son: {', '.join(map(str, numeros_ganadores))}")

        # Comparar con números del usuario
        opcion = input("¿Desea ingresar sus propios números para comparar? (s/n): ").lower()
        if opcion == "s":
            boletos = list(map(int, input(f"Ingrese sus {cantidad} números separados por comas: ").split(',')))

            # Comparar boletos con los números ganadores
            aciertos = set(numeros_ganadores) & set(boletos)
            print(f"Acertaste {len(aciertos)} número(s): {', '.join(map(str, aciertos)) if aciertos else 'Ninguno'}")
        else:
            print("¡Gracias por participar!")
    except ValueError:
        print("Entrada no válida. Intente de nuevo.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

if __name__ == "__main__":
    main()
