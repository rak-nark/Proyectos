package handlers

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

func ProtectedRoute(c *gin.Context) {
	userEmail, _ := c.Get("userEmail") // Obtenido del middleware

	c.JSON(http.StatusOK, gin.H{
		"message": "¡Ruta protegida!",
		"user":    userEmail,
	})
}