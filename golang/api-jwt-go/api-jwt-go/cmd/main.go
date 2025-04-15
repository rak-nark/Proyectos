package main

import (
    "bytes"
    "fmt"
    "io"
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

    // Deshabilitar el logging de Gin
    gin.DefaultWriter = os.Stdout
    gin.DisableConsoleColor()

    r := gin.Default()
    r.Use(func(c *gin.Context) {
        // Solo para rutas que necesitan preservar el body
        if c.Request.URL.Path == "/api/logout" || c.Request.URL.Path == "/api/refresh" {
            // Leer y reescribir el body
            bodyBytes, _ := io.ReadAll(c.Request.Body)
            c.Request.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))
        }
        c.Next()
    })

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
    frontendPath := "../frontend"
    r.Static("/frontend", frontendPath)
    // Redirigir la raíz ("/") a "/frontend/index.html"
    r.GET("/", func(c *gin.Context) {
        c.Redirect(302, "/frontend/index.html")
    })

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

    // Obtener puerto
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    // Mostrar mensaje limpio
    fmt.Printf("\n🚀 Servidor listo para pruebas\n")
    fmt.Printf("🔗 Endpoint del backend: http://localhost:%s\n", port)
    fmt.Printf("🌐 Frontend disponible en: http://localhost:%s/frontend\n", port)

    // Iniciar servidor
    r.Run(":" + port)
}