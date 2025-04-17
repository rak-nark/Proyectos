package main

import(
"fmt"
"os"
)

func main(){
	dir, err := os.Open(".")
	if err != nil{
		fmt.Println("Error ala Abrir el Directorio:", err)
		return
	}
	defer dir.Close()

	archivos, err := dir.Readdir(-1)
	if err != nil{
		fmt.Println("Error ala Leer Arcivos: ",err)
		return
	}

	fmt.Println("Archivos en el Directorio Actual: ")
	for _, arcarchivo := range archivos{
		fmt.Println(arcarchivo.Name())
	}



}