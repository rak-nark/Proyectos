package main

import (
	"fmt"
	"math"
	"os"
	"os/exec"
	"time"
)

func main() {
	// Configura el Command Prompt (requiere ejecutar como administrador)
	exec.Command("cmd", "/c", "mode con: cols=80 lines=25").Run()
	exec.Command("cmd", "/c", "color 07").Run() // Fondo negro, texto blanco

	const (
		width, height = 80, 24
		R1, R2        = 1, 2
		K1, K2        = 15, 5  // Ajustados para CMD
	)

	var A, B float64
	buffer := make([]rune, width*height)
	zBuffer := make([]float64, width*height)
	
	// Caracteres de iluminación (optimizados para CMD)
	shades := []rune(".,-~:;=!*#$@")

	for {
		// Limpieza manual de pantalla (alternativa para Windows)
		clearCMD()
		
		for i := range buffer {
			buffer[i] = ' '
			zBuffer[i] = 0
		}

		sinA, cosA := math.Sin(A), math.Cos(A)
		sinB, cosB := math.Sin(B), math.Cos(B)

		// Paso angular más grueso para mejor rendimiento
		for theta := 0.0; theta < 2*math.Pi; theta += 0.05 {
			sinTheta, cosTheta := math.Sin(theta), math.Cos(theta)
			for phi := 0.0; phi < 2*math.Pi; phi += 0.02 {
				sinPhi, cosPhi := math.Sin(phi), math.Cos(phi)

				// Coordenadas 3D + rotación
				x := (R2 + R1*cosTheta) * cosPhi
				y := (R2 + R1*cosTheta) * sinPhi
				z := R1 * sinTheta

				xRot := x*cosA*cosB - y*sinB + z*sinA*cosB
				yRot := x*cosA*sinB + y*cosB + z*sinA*sinB
				zRot := -x*sinA + z*cosA + K2

				factor := 1 / zRot
				xProj := int(width/2 + K1*factor*xRot)
				yProj := int(height/2 - K1*factor*yRot)

				if xProj >= 0 && xProj < width && yProj >= 0 && yProj < height {
					idx := yProj*width + xProj
					if factor > zBuffer[idx] {
						zBuffer[idx] = factor
						// Iluminación simplificada (mejor visibilidad en CMD)
						light := cosTheta*cosPhi*cosA*sinB + sinPhi*cosB - sinTheta*cosPhi*sinA*sinB
						if light > 0 {
							luminance := int(light * float64(len(shades)-1))
							buffer[idx] = shades[luminance]
						}
					}
				}
			}
		}

		// Dibuja el frame línea por línea (evita desbordamiento)
		for y := 0; y < height; y++ {
			line := make([]rune, width)
			for x := 0; x < width; x++ {
				line[x] = buffer[y*width+x]
			}
			fmt.Println(string(line))
		}

		A += 0.04
		B += 0.02
		time.Sleep(30 * time.Millisecond)  // 30 FPS (óptimo para CMD)
	}
}

// clearCMD limpia la pantalla en Windows (sin ANSI)
func clearCMD() {
	cmd := exec.Command("cmd", "/c", "cls")
	cmd.Stdout = os.Stdout
	cmd.Run()
}