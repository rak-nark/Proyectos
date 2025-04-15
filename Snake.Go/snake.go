package main

import (
	"fmt"
	"github.com/nsf/termbox-go"
	"math/rand"
	"time"
)

// Constantes
const (
	width  = 20
	height = 10
)

// Direcciones
type Direction int

const (
	Up Direction = iota
	Down
	Left
	Right
)

// Snake
type Snake struct {
	body      []Position
	direction Direction
}

// Comida
type Position struct {
	x, y int
}

var (
	snake    Snake
	food     Position
	gameOver bool
	score    int
)

func main() {
	// Inicializar termbox
	err := termbox.Init()
	if err != nil {
		panic(err)
	}
	defer termbox.Close()

	initGame()

	// Goroutine para input
	inputChan := make(chan Direction)
	go handleInput(inputChan)

	// Bucle principal
	ticker := time.NewTicker(100 * time.Millisecond) // 10 FPS
	defer ticker.Stop()

	for !gameOver {
		select {
		case dir := <-inputChan:
			changeDirection(dir)
		case <-ticker.C:
			update()
			render()
		}
	}

	fmt.Printf("Game Over! Puntaje: %d\n", score)
}

func initGame() {
	snake = Snake{
		body:      []Position{{x: width / 2, y: height / 2}},
		direction: Right,
	}
	placeFood()
	gameOver = false
	score = 0
}

func placeFood() {
	rand.Seed(time.Now().UnixNano())
	food = Position{
		x: rand.Intn(width),
		y: rand.Intn(height),
	}
}

func handleInput(inputChan chan Direction) {
	for {
		ev := termbox.PollEvent()
		if ev.Type == termbox.EventKey {
			switch ev.Key {
			case termbox.KeyArrowUp:
				inputChan <- Up
			case termbox.KeyArrowDown:
				inputChan <- Down
			case termbox.KeyArrowLeft:
				inputChan <- Left
			case termbox.KeyArrowRight:
				inputChan <- Right
			case termbox.KeyEsc:
				gameOver = true
				return
			}
		}
	}
}

func changeDirection(dir Direction) {
	// Evitar que el snake gire 180 grados
	if (dir == Up && snake.direction != Down) ||
		(dir == Down && snake.direction != Up) ||
		(dir == Left && snake.direction != Right) ||
		(dir == Right && snake.direction != Left) {
		snake.direction = dir
	}
}

func update() {
	head := snake.body[0]
	var newHead Position

	switch snake.direction {
	case Up:
		newHead = Position{x: head.x, y: head.y - 1}
	case Down:
		newHead = Position{x: head.x, y: head.y + 1}
	case Left:
		newHead = Position{x: head.x - 1, y: head.y}
	case Right:
		newHead = Position{x: head.x + 1, y: head.y}
	}

	// Check colisiones
	if newHead.x < 0 || newHead.x >= width || newHead.y < 0 || newHead.y >= height {
		gameOver = true
		return
	}

	for _, segment := range snake.body {
		if segment == newHead {
			gameOver = true
			return
		}
	}

	// Mover snake
	snake.body = append([]Position{newHead}, snake.body...)

	// Comer comida
	if newHead == food {
		score++
		placeFood()
	} else {
		// Quitar cola si no comió
		snake.body = snake.body[:len(snake.body)-1]
	}
}

func render() {
	termbox.Clear(termbox.ColorDefault, termbox.ColorDefault)

	// Dibujar snake
	for _, pos := range snake.body {
		termbox.SetCell(pos.x, pos.y, '■', termbox.ColorGreen, termbox.ColorDefault)
	}

	// Dibujar comida
	termbox.SetCell(food.x, food.y, '●', termbox.ColorRed, termbox.ColorDefault)

	// Dibujar bordes
	for x := 0; x < width; x++ {
		termbox.SetCell(x, -1, '─', termbox.ColorWhite, termbox.ColorDefault)
		termbox.SetCell(x, height, '─', termbox.ColorWhite, termbox.ColorDefault)
	}
	for y := 0; y < height; y++ {
		termbox.SetCell(-1, y, '│', termbox.ColorWhite, termbox.ColorDefault)
		termbox.SetCell(width, y, '│', termbox.ColorWhite, termbox.ColorDefault)
	}

	// Mostrar puntaje
	scoreStr := fmt.Sprintf("Puntaje: %d", score)
	for i, ch := range scoreStr {
		termbox.SetCell(width/2+i, height+1, ch, termbox.ColorYellow, termbox.ColorDefault)
	}

	termbox.Flush()
}
