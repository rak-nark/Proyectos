package main

import (
	"os"
	"time"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/rak-nark/proyectos/internal/handlers"
	"github.com/rak-nark/proyectos/internal/middleware"
)

func main() {
	// Configuración para producción
	gin.SetMode(gin.ReleaseMode)

	r := gin.Default()
	
	// Middlewares
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Authorization", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))
	r.SetTrustedProxies([]string{"127.0.0.1"})

	// Archivos estáticos (frontend)
	r.Static("/frontend", "./frontend")

	// Rutas públicas
	r.POST("/register", handlers.Register)
	r.POST("/login", handlers.Login)

	// Rutas protegidas
	protected := r.Group("/api")
	protected.Use(middleware.AuthMiddleware())
	{
		protected.GET("/protected", handlers.ProtectedRoute)
		protected.POST("/refresh", handlers.RefreshToken)
		protected.POST("/logout", handlers.Logout)
		protected.GET("/profile", handlers.GetProfile)
		protected.PUT("/update-password", handlers.UpdatePassword)
		protected.DELETE("/account", handlers.DeleteAccount)
	}

	// Inicia el servidor
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	r.Run(":" + port)
}