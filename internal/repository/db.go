package repository
import (
    "database/sql"
    "fmt"
     _"github.com/go-sql-driver/mysql" // Driver MySQL
)
const (
    dbUser     = "root"
    dbPassword = ""          // Si configuraste contraseña en XAMPP, colócala aquí
    dbName     = "jwt_api"
)

func InitDB() (*sql.DB, error) {
    // Formato: "usuario:contraseña@tcp(host:puerto)/nombre_db"
    connStr := fmt.Sprintf("%s:%s@tcp(127.0.0.1:3306)/%s", dbUser, dbPassword, dbName)
    
    db, err := sql.Open("mysql", connStr)
    if err != nil {
        return nil, fmt.Errorf("error al conectar a MySQL: %v", err)
    }

    // Verificar que la conexión funcione
    err = db.Ping()
    if err != nil {
        return nil, fmt.Errorf("error al hacer ping a MySQL: %v", err)
    }

    fmt.Println("✅ Conexión a MySQL establecida")
    return db, nil
}