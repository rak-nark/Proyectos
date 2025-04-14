package main

import(
	"fmt"
	"strings"
)

func main(){
	var palabra string
	fmt.Print("Ingrese una Palabra")
	fmt.Scan(&palabra)

	palabra=strings.ToLower(palabra)
	esPalindromo := true

	for i := 0 ;i < len(palabra)/2; i++{
		if palabra[i] != palabra[len(palabra)-1-i]{
			esPalindromo = false
			break
		}
	}

	if esPalindromo{
		fmt.Println("Es Palindromo")

	}else{
		fmt.Println("No es Palindromo")
	}





}