package main

import (
	"fmt"
)

func main() {
	var a, b float64
	var op string

	fmt.Print("Ingrese el Primer Número: ")
	_, err := fmt.Scanln(&a)
	if err != nil {
		fmt.Println("Error al leer el primer número:", err)
		return
	}

	fmt.Print("Ingrese el Segundo Número: ")
	_, err = fmt.Scanln(&b)
	if err != nil {
		fmt.Println("Error al leer el segundo número:", err)
		return
	}

	fmt.Print("Operacion ( + , - , * , / ): ")
	_, err = fmt.Scanln(&op)
	if err != nil {
		fmt.Println("Error al leer la operación:", err)
		return
	}

	switch op {
	case "+":
		fmt.Println("Resultado: ", a+b)
	case "-":
		fmt.Println("Resultado: ", a-b)
	case "*":
		fmt.Println("Resultado: ", a*b)
	case "/":
		if b != 0 {
			fmt.Println("Resultado: ", a/b)
		} else {
			fmt.Println("Error: división por 0")
		}
	default:
		fmt.Println("Operacion no Valida")
	}
}