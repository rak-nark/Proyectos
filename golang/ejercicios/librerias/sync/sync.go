package main

import (
    "fmt"
    "sync"
    "time"
)

func tarea(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Printf("Tarea %d iniciada\n", id)
    time.Sleep(2 * time.Second)
    fmt.Printf("Tarea %d completada\n", id)
}

func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go tarea(i, &wg)
    }

    wg.Wait()
    fmt.Println("Todas las tareas completadas")
}