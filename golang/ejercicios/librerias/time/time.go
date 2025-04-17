package main

import(
	"fmt"
	"time"
)

func main(){
	hoy := time.Now()
	cumple := time.Date(hoy.Year(), time.September, 2, 0, 0, 0, 0 ,time.Local)

	if hoy.After(cumple){
		cumple = cumple.AddDate(1, 0, 0)
	}

	diasFaltantes := int(cumple.Sub(hoy).Hours()/24)
	fmt.Printf("Faltan %d dias para tu cumpleaños.\n", diasFaltantes)



}