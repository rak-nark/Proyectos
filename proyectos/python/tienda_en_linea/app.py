from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "tienda_en_linea"

mysql = MySQL(app)

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()
    return render_template("index.html", productos=productos)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        contrasena_hash = generate_password_hash(contrasena)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)", (nombre, email, contrasena_hash))
        mysql.connection.commit()
        cur.close()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", [email])
        usuario = cur.fetchone()
        cur.close()

        if usuario and check_password_hash(usuario[3], contrasena):
            session["usuario_id"] = usuario[0]
            flash("Bienvenido de nuevo", "success")
            return redirect(url_for("carrito"))
        else:
            flash("Correo o contraseña incorrectos", "error")

    return render_template("login.html")

@app.route("/carrito")
def carrito():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.nombre, p.precio, c.cantidad, p.imagen, p.fecha_creacion
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s LIMIT 25
    """, [usuario_id])
    carrito_items = cur.fetchall()
    cur.close()

    total = sum(item[2] * item[3] for item in carrito_items)
    total = int(total)

    carrito_items = [
        (item[1], item[2], item[3], item[4], item[5].strftime('%Y-%m-%d %H:%M:%S') if item[5] else 'N/A')
        for item in carrito_items
    ]

    return render_template("carrito.html", carrito_items=carrito_items, total=total)

@app.route("/tienda")
def tienda():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para acceder a la tienda", "warning")
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()

    return render_template("index.html", productos=productos)

@app.route("/agregar-al-carrito", methods=["POST"])
def agregar_al_carrito():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    producto_id = request.form["producto_id"]
    cantidad = request.form["cantidad"]
    usuario_id = session["usuario_id"]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)", (usuario_id, producto_id, cantidad))
    mysql.connection.commit()
    cur.close()

    flash("Producto agregado al carrito", "success")
    return redirect(url_for("tienda"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

















