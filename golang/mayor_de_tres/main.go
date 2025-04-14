package main

import "fmt"

func main() {
	var a, b, c int
	fmt.Print("Ingresa el Primer Número")
	fmt.Scan(&a)
	fmt.Print("Ingresa el Segundo Número")
	fmt.Scan(&b)
	fmt.Print("Ingresa el Tercer Número")
	fmt.Scan(&c)

	mayor := a

	if b > mayor {
		mayor = b
	}
	if c > mayor {
		mayor = c
	}
	fmt.Println("El Mayor es: ", mayor)

}
