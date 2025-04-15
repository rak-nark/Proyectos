package handlers

import (
	
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/rak-nark/proyectos/internal/repository" // Importa tu repositorio de la base de datos
	"github.com/rak-nark/proyectos/pkg/utils"
	"golang.org/x/crypto/bcrypt"
)

func Register(c *gin.Context) {
	var user struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}

	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Datos inválidos"})
		return
	}

	// Hashear la contraseña
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al hashear la contraseña"})
		return
	}

	// Guardar en MySQL
	db, err := repository.InitDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al conectar a la DB"})
		return
	}
	defer db.Close()

	_, err = db.Exec("INSERT INTO users (email, password) VALUES (?, ?)", user.Email, string(hashedPassword))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "El usuario ya existe o hay un error en la DB"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Usuario registrado con éxito!"})
}
func Login(c *gin.Context) {
	var user struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}

	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Datos inválidos"})
		return
	}

	// 1. Conectar a la base de datos
	db, err := repository.InitDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al conectar a la DB"})
		return
	}
	defer db.Close()

	// 2. Buscar usuario en la DB (ahora incluyendo el ID)
	var storedUser struct {
		ID       int
		Email    string
		Password string
	}
	err = db.QueryRow("SELECT id, email, password FROM users WHERE email = ?", user.Email).Scan(
		&storedUser.ID,
		&storedUser.Email,
		&storedUser.Password,
	)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Usuario no encontrado"})
		return
	}

	// 3. Verificar contraseña
	if err := bcrypt.CompareHashAndPassword([]byte(storedUser.Password), []byte(user.Password)); err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Contraseña incorrecta"})
		return
	}

	// 4. Generar JWT
	token, err := utils.GenerateToken(storedUser.Email)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al generar token"})
		return
	}
	_, err = db.Exec("DELETE FROM refresh_tokens WHERE user_id = ?", storedUser.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al limpiar refresh tokens antiguos"})
		return
	}
	// 5. Generar y guardar refresh token (requiere github.com/google/uuid)
	refreshToken := uuid.New().String()
	expiresAt := time.Now().Add(7 * 24 * time.Hour) // Expira en 7 días

	_, err = db.Exec(
		"INSERT INTO refresh_tokens (token, user_id, expires_at) VALUES (?, ?, ?)",
		refreshToken,
		storedUser.ID,
		expiresAt,
	)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al guardar refresh token"})
		return
	}

	// 6. Devolver ambos tokens
	c.JSON(http.StatusOK, gin.H{
		"token":         token,
		"refresh_token": refreshToken,
	})
}
func RefreshToken(c *gin.Context) {
	// 1. Conectar a la DB
	db, err := repository.InitDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al conectar a la DB"})
		return
	}
	defer db.Close()

	// 2. Parsear el refresh token del body
	var body struct {
		RefreshToken string `json:"refresh_token"`
	}
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Datos inválidos"})
		return
	}

	// 3. Verificar el refresh token en la DB
	var userID int
	err = db.QueryRow(
		"SELECT user_id FROM refresh_tokens WHERE token = ? AND expires_at > NOW()",
		body.RefreshToken,
	).Scan(&userID)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Refresh token inválido o expirado"})
		return
	}

	// 4. Obtener el email del usuario
	var userEmail string
	err = db.QueryRow("SELECT email FROM users WHERE id = ?", userID).Scan(&userEmail)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Usuario no encontrado"})
		return
	}

	// 5. Generar nuevo JWT
	newToken, err := utils.GenerateToken(userEmail)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al generar token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"token": newToken})
}
func Logout(c *gin.Context) {
    var request struct {
        RefreshToken string `json:"refresh_token" binding:"required"`
    }

    // Binding directo (el middleware ya preservó el body)
    if err := c.ShouldBindJSON(&request); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{
            "error": "Datos inválidos",
            "solution": "Envía un JSON con formato: {\"refresh_token\":\"tu_token\"}",
        })
        return
    }

    db, err := repository.InitDB()
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error de conexión a DB"})
        return
    }
    defer db.Close()

    // Operación directa DELETE (optimizada)
    if _, err := db.Exec("DELETE FROM refresh_tokens WHERE token = ?", request.RefreshToken); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{
            "error": "Error al revocar token",
            "details": err.Error(),
        })
        return
    }

    c.JSON(http.StatusOK, gin.H{"message": "Sesión cerrada exitosamente"})
}

// handlers/profile.go
func GetProfile(c *gin.Context) {
	userEmail, exists := c.Get("userEmail")
	if !exists {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No se pudo obtener el usuario"})
		return
	}

	email, ok := userEmail.(string)
	if !ok || email == "" {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Email inválido"})
		return
	}

	db, err := repository.InitDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error de conexión a DB"})
		return
	}
	defer db.Close()

	var profile struct {
		Email string `json:"email"`
		// Eliminamos CreatedAt temporalmente
	}

	// Consulta modificada
	err = db.QueryRow(`
        SELECT email 
        FROM users 
        WHERE email = ?`,
		email,
	).Scan(&profile.Email)

	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "Error al buscar usuario",
			"details": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{"profile": profile})
}
func UpdatePassword(c *gin.Context) {
	// 1. Parsear datos
	var body struct {
		CurrentPassword string `json:"current_password"`
		NewPassword     string `json:"new_password"`
	}
	if err := c.ShouldBindJSON(&body); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Datos inválidos"})
		return
	}

	// 2. Verificar usuario y contraseña actual
	userEmail, _ := c.Get("userEmail")
	db, err := repository.InitDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error de conexión a DB"})
		return
	}
	defer db.Close()

	var currentHashedPassword string
	err = db.QueryRow("SELECT password FROM users WHERE email = ?", userEmail).Scan(&currentHashedPassword)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Usuario no encontrado"})
		return
	}

	// 3. Validar contraseña actual
	if err := bcrypt.CompareHashAndPassword([]byte(currentHashedPassword), []byte(body.CurrentPassword)); err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Contraseña actual incorrecta"})
		return
	}

	// 4. Hashear nueva contraseña
	newHashedPassword, err := bcrypt.GenerateFromPassword([]byte(body.NewPassword), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al hashear contraseña"})
		return
	}

	// 5. Actualizar en DB
	_, err = db.Exec("UPDATE users SET password = ? WHERE email = ?", newHashedPassword, userEmail)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al actualizar contraseña"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Contraseña actualizada con éxito"})
}
func DeleteAccount(c *gin.Context) {
	userEmail, _ := c.Get("userEmail")

	db, err := repository.InitDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error de conexión a DB"})
		return
	}
	defer db.Close()

	// Eliminar usuario y sus tokens asociados
	_, err = db.Exec("DELETE FROM refresh_tokens WHERE user_id = (SELECT id FROM users WHERE email = ?)", userEmail)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al eliminar tokens"})
		return
	}

	_, err = db.Exec("DELETE FROM users WHERE email = ?", userEmail)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al eliminar cuenta"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Cuenta eliminada con éxito"})
}
