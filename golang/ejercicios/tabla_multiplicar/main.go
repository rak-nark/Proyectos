package main

import "fmt"

func main() {
    var n int
    fmt.Print("Ingresa un número para la tabla de multiplicar: ")
    fmt.Scan(&n)

    fmt.Printf("Tabla de multiplicar del %d:\n", n)
    for i := 1; i <= 10; i++ {
        fmt.Printf("%d x %d = %d\n", n, i, n*i)
    }
}
