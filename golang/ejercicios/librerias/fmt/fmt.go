package main

import "fmt"

func main (){
	var nombre string
	var edad int

	fmt.Print("Ingrese su Nombre: ")
	fmt.Scan(&nombre)

	fmt.Print("Ingrese su Edad: ")
	fmt.Scan(&edad)

	fmt.Printf("Hola, %s. Tienes %d años.\n", nombre, edad)

}