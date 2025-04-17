package main

import (
	"encoding/json"
	"fmt"
	
)

type Persona struct{
	Nombre string `json:"nombre"`
    Edad   int    `json:"edad"`
}
func main(){
	p := Persona{"juan",30}
	jsonData,_:= json.Marshal(p)
	fmt.Println("JSON:", string(jsonData))

	var p2 Persona
	jsonSrt :=  `{"nombre":"Ana","edad":25}`
	json.Unmarshal([]byte(jsonSrt),&p2)
	fmt.Printf("Struct: %+v\n", p2)
}