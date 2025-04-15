package middleware

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/rak-nark/proyectos/pkg/utils"
)

// middleware/auth.go
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Token no proporcionado"})
            return
        }

        tokenString := strings.TrimPrefix(authHeader, "Bearer ")
        claims, err := utils.ValidateToken(tokenString)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
                "error": "Token inválido",
                "details": err.Error(),
            })
            return
        }

        // Verificamos que el email esté en los claims
        if claims.Email == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Token no contiene email"})
            return
        }

        c.Set("userEmail", claims.Email)
        c.Next()
    }
}