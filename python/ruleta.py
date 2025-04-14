import random

# Datos del jugador
saldo = 1000

# Función para mostrar el menú
def menu():
    print("\n--- Simulador de Casino ---")
    print("1. Jugar a la Ruleta")
    print("2. Jugar al Blackjack")
    print("3. Jugar a las Tragamonedas")
    print("4. Salir")
    opcion = input("Elige una opción: ")
    return opcion

# Función para jugar a la ruleta
def jugar_ruleta():
    global saldo
    print("\n--- Ruleta ---")
    print(f"Saldo actual: ${saldo}")

    try:
        apuesta = int(input("Ingresa tu apuesta: "))
        if apuesta > saldo or apuesta <= 0:
            print("Apuesta no válida.")
            return

        tipo_apuesta = input("Apuesta a (rojo, negro, par, impar, número): ").lower()
        numero_apuesta = None
        if tipo_apuesta == 'número':
            numero_apuesta = int(input("Elige un número (0-36): "))
            if numero_apuesta < 0 or numero_apuesta > 36:
                print("Número no válido.")
                return

        print("Girando la ruleta...")
        numero_ganador = random.randint(0, 36)
        color_ganador = 'rojo' if numero_ganador % 2 == 0 else 'negro'
        paridad_ganador = 'par' if numero_ganador % 2 == 0 else 'impar'

        print(f"Número ganador: {numero_ganador} ({color_ganador}, {paridad_ganador})")

        # Verificar resultados
        if tipo_apuesta == 'rojo' and color_ganador == 'rojo':
            saldo += apuesta
            print("Ganaste!")
        elif tipo_apuesta == 'negro' and color_ganador == 'negro':
            saldo += apuesta
            print("Ganaste!")
        elif tipo_apuesta == 'par' and paridad_ganador == 'par':
            saldo += apuesta
            print("Ganaste!")
        elif tipo_apuesta == 'impar' and paridad_ganador == 'impar':
            saldo += apuesta
            print("Ganaste!")
        elif tipo_apuesta == 'número' and numero_apuesta == numero_ganador:
            saldo += apuesta * 35
            print("Ganaste mucho!")
        else:
            saldo -= apuesta
            print("Perdiste.")
    except ValueError:
        print("Entrada no válida.")

# Función para jugar al Blackjack
def jugar_blackjack():
    global saldo
    print("\n--- Blackjack ---")
    print(f"Saldo actual: ${saldo}")

    try:
        apuesta = int(input("Ingresa tu apuesta: "))
        if apuesta > saldo or apuesta <= 0:
            print("Apuesta no válida.")
            return

        jugador = random.randint(15, 21)
        crupier = random.randint(17, 21)
        print(f"Tus puntos: {jugador}")
        print(f"Puntos del crupier: {crupier}")

        if jugador > 21:
            saldo -= apuesta
            print("Te pasaste. Perdiste.")
        elif jugador > crupier or crupier > 21:
            saldo += apuesta
            print("Ganaste!")
        else:
            saldo -= apuesta
            print("Perdiste.")
    except ValueError:
        print("Entrada no válida.")

# Función para jugar a las tragamonedas
def jugar_tragamonedas():
    global saldo
    print("\n--- Tragamonedas ---")
    print(f"Saldo actual: ${saldo}")

    try:
        apuesta = int(input("Ingresa tu apuesta: "))
        if apuesta > saldo or apuesta <= 0:
            print("Apuesta no válida.")
            return

        print("Girando...")
        resultados = [random.choice(['🍒', '🍋', '🔔', '⭐', '💎']) for _ in range(3)]
        print(" | ".join(resultados))

        if len(set(resultados)) == 1:
            saldo += apuesta * 10
            print("Jackpot! Ganaste mucho!")
        elif len(set(resultados)) == 2:
            saldo += apuesta * 2
            print("Ganaste algo!")
        else:
            saldo -= apuesta
            print("Perdiste.")
    except ValueError:
        print("Entrada no válida.")

# Bucle principal
def iniciar_casino():
    while True:
        opcion = menu()
        if opcion == '1':
            jugar_ruleta()
        elif opcion == '2':
            jugar_blackjack()
        elif opcion == '3':
            jugar_tragamonedas()
        elif opcion == '4':
            print("Gracias por jugar. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

# Iniciar el simulador
if __name__ == "__main__":
    iniciar_casino()







        
