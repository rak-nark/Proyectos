package utils

import (
	"time"
	"github.com/dgrijalva/jwt-go"
)

// Clave secreta (¡cámbiala en producción!)
var jwtKey = []byte("mi_clave_secreta_super_segura")

// Claims define la estructura del token JWT
type Claims struct {
	Email string `json:"email"`
	jwt.StandardClaims
}

// GenerateToken genera un nuevo JWT para el email proporcionado
func GenerateToken(email string) (string, error) {
	expirationTime := time.Now().Add(24 * time.Hour) // Token expira en 24h

	claims := &Claims{
		Email: email,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtKey)
}

// ValidateToken verifica si un token es válido
func ValidateToken(tokenString string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
		return jwtKey, nil
	})

	if claims, ok := token.Claims.(*Claims); ok && token.Valid {
		return claims, nil
	}

	return nil, err
}