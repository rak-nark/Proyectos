package main

import "fmt"

func main() {
    var num int
    fmt.Print("Ingresa un número: ")
    fmt.Scan(&num)

    if num <= 1 {
        fmt.Println("No es primo")
        return
    }

    esPrimo := true
    for i := 2; i*i <= num; i++ {
        if num%i == 0 {
            esPrimo = false
            break
        }
    }

    if esPrimo {
        fmt.Println(num, "es un número primo.")
    } else {
        fmt.Println(num, "no es primo.")
    }
}
