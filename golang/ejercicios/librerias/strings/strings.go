package main

import(
	"fmt"
	"strings"
)

func main(){
	texto := "Go es genial. Go es rápido. Go es simple."
	palabra := "Go"

	conteo:= strings.Count(texto,palabra)
	fmt.Printf("La Palabra '%s' aparece %d veces\n", palabra, conteo)

}