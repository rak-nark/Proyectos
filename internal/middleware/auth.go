package middleware

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/rak-nark/proyectos/pkg/utils"
)

func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Extrae el token del header "Authorization"
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Token no proporcionado"})
            c.Abort()
            return
        }

        // Elimina "Bearer " si está presente
        tokenString := strings.TrimPrefix(authHeader, "Bearer ")

        // Valida el token
        claims, err := utils.ValidateToken(tokenString)
        if err != nil {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Token inválido: " + err.Error()})
            c.Abort()
            return
        }

        c.Set("userEmail", claims.Email)
        c.Next()
    }
}