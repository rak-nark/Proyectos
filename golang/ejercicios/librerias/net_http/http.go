package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hola, mundo!")
}

func main() {
    http.HandleFunc("/", handler)
    fmt.Println("Servidor iniciado en http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}