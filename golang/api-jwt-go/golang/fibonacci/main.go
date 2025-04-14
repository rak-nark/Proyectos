package main

import "fmt"

func main() {
	var n int
	fmt.Print("¿Cuantos terminos de Fibonacci quiere?")
	fmt.Scan(&n)

	a, b := 0, 1
	fmt.Print("Serie: ")
	for i := 0; i < n; i++ {
		fmt.Print(a, "")
		a, b = b, a+b
	}
	fmt.Println()

}
