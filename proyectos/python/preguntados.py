import json
import time
import random
import csv

preguntas ={
    "Ciencia": [
        {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "opciones": ["Tierra", "Júpiter", "Marte", "Saturno"], "respuesta": "Júpiter"},
        {"pregunta": "¿Qué molécula transporta oxígeno en la sangre?", "opciones": ["Agua", "Hemoglobina", "Glucosa", "ADN"], "respuesta": "Hemoglobina"}
    ],
    "Historia": [
        {"pregunta": "¿En qué año comenzó la Segunda Guerra Mundial?", "opciones": ["1939", "1914", "1945", "1929"], "respuesta": "1939"},
        {"pregunta": "¿Quién fue el primer presidente de los Estados Unidos?", "opciones": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"], "respuesta": "George Washington"}
    ],
    "Cultura Popular": [
        {"pregunta": "¿Quién es el autor de la saga de Harry Potter?", "opciones": ["J.K. Rowling", "George R.R. Martin", "Stephen King", "Suzanne Collins"], "respuesta": "J.K. Rowling"},
        {"pregunta": "¿Qué banda compuso la canción 'Bohemian Rhapsody'?", "opciones": ["Queen", "The Beatles", "Pink Floyd", "Led Zeppelin"], "respuesta": "Queen"}
    ]
}

def guardar_ranking(nombre, puntuacion):
    with open("ranking.csv", mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([nombre, puntuacion])

def mostrar_ranking():
    try:
        with open("ranking.csv",mode="r",encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            print("\n--- Ranking de Jugadores ---")
            for fila in sorted(lector, key=lambda x: int(x[1]), reverse=True):
                print(f"{fila[0]}:{fila[1]}puntos")
    except FileExistsError:
        print("\nNo hay datos en el ranking aún.")

def jugar():
    print("\n¡Bienvenido al juego de preguntas y respuestas!")
    nombre = input("Por favor, ingresa tu nombre: ")
    puntuacion = 0

    while True:
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(preguntas.keys(), start=1):
            print(f"{i}. {categoria}")

        eleccion = input("Elige una categoría (1/2/3 o 'salir' para terminar): ").strip().lower()

        if eleccion == "salir":
            break

        try:
            categoria_seleccionada = list(preguntas.keys())[int(eleccion) - 1]
        except (IndexError, ValueError):
            print("\n¡Opción no válida! Intenta de nuevo.")
            continue

        print(f"\nHas elegido: {categoria_seleccionada}\n")
        preguntas_categoria = random.sample(preguntas[categoria_seleccionada], len(preguntas[categoria_seleccionada]))

        for pregunta in preguntas_categoria:
            print(f"\n{pregunta['pregunta']}")
            for i, opcion in enumerate(pregunta['opciones'], start=1):
                print(f"{i}. {opcion}")

            tiempo_inicio = time.time()
            respuesta = input("Tu respuesta (1/2/3/4): ").strip()
            tiempo_fin = time.time()

            try:
                respuesta_seleccionada = pregunta['opciones'][int(respuesta) - 1]
            except (IndexError, ValueError):
                print("\nRespuesta no válida. No obtuviste puntos.")
                continue

            if respuesta_seleccionada == pregunta['respuesta']:
                tiempo_respuesta = tiempo_fin - tiempo_inicio
                puntos = 10
                if tiempo_respuesta <= 5:
                    puntos += 5
                print(f"\n¡Correcto! Ganaste {puntos} puntos.")
                puntuacion += puntos
            else:
                print(f"\nIncorrecto. La respuesta correcta era: {pregunta['respuesta']}")

    print(f"\nJuego terminado. Tu puntuación final es: {puntuacion} puntos.")
    guardar_ranking(nombre, puntuacion)
    mostrar_ranking()

if __name__ == "__main__":
    jugar()

