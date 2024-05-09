from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    session,
)
import os
import config
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración para la primera base de datos
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_DB"] = config.MYSQL_DB2  # cambio de BD
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["SECRET_KEY"] = config.HEX_SEC_KEY
mysql = MySQL(app)


# Seccion de inicio pagina web
@app.route("/")
def inicio():
    return render_template("inicio/inicio.html")


@app.route("/ubicacion")
def ubicacion():
    return render_template("inicio/ubicacion.html")


@app.route("/contacto")
def contacto():
    return render_template("inicio/contacto.html")


@app.route("/problematica")
def problematica():
    return render_template("inicio/problematica.html")


# Seccion del gestor
@app.route("/tablero")
def tablero():
    if "email" in session:
        # si se registro se envia a tablero con una session creada
        return render_template("tablero.html", email=session["email"])
    else:
        return render_template("iniciar_sesion.html")


@app.route("/inventario", methods=['GET'])
def inventario():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Producto")
        Productos = cur.fetchall()
        cur.close()
        return render_template('inventario.html', Productos=Productos)
    else:
        return render_template("iniciar_sesion.html")


@app.route('/clientes', methods=['GET'])
def clientes():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        cur.close()
        return render_template('clientes.html', clientes=clientes)
    else:
        return render_template("iniciar_sesion.html")
    
    
@app.route('/ventas', methods=['GET'])
def ventas():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ventas")
        ventas = cur.fetchall()
        cur.close()
        return render_template('ventas.html', ventas=ventas)
    else:
        return render_template("iniciar_sesion.html")


@app.route('/categorias', methods=['GET'])
def categorias():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM categorias")
        categorias = cur.fetchall()
        cur.close()
        return render_template('categorias.html', categorias=categorias)
    else:
        return render_template("iniciar_sesion.html")



# Registro y login
@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":  # lo que recibo por post
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        cur = mysql.connection.cursor()  # Guardar conexion en variable
        cur.execute("SELECT * FROM login WHERE Correo = %s", (correo,))
        existing_email = cur.fetchone()  # Si existe, Guardar la tupla
        cur.close()
        print(existing_email)

        if not existing_email:
            # El correo electrónico no está registrado
            correo_no_encontrado = True
            return render_template("iniciar_sesion.html", correo_no_encontrado=correo_no_encontrado)
        else:
            # El correo electrónico está registrado
            # En el cuarto campo de la tupla (Contraseña) se compara con la contraseña del Form
            if existing_email[3] == contraseña:
                # Contraseña correcta
                # Crear session email con el email
                session["email"] = correo
                return render_template("iniciar_sesion.html", user=correo, registration_login=True)
            else:
                # Contraseña incorrecta
                bad_password = True
                return render_template(
                    "iniciar_sesion.html", bad_password=bad_password, email=correo
                )
    return render_template("iniciar_sesion.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    # if "email" in session:
    #     return render_template("tablero.html", email=session["email"])
    # else:
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")

        # comprobar antes si estan en la bd para no registralos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE Correo = %s", (correo,))
        existing_email = cur.fetchone()

        cur.execute("SELECT * FROM login WHERE Nombre = %s", (nombre,))
        existing_user = cur.fetchone()

        if existing_email:  # ya existe en bd
            email_found = True
            error_message = "El correo electrónico ya está registrado"
            return render_template(
                "registro.html", email_found=email_found, error_message=error_message
            )

        elif existing_user:  # ya exis  te usuario
            user_found = True
            error_message = "El usuario ya existe. Por favor, elija otro"
            return render_template(
                "registro.html", user_found=user_found, error_message=error_message
            )
        else:
            # registrar en base de datos
            cur.execute(
                "INSERT INTO login (Nombre, Correo, Contraseña) VALUES (%s, %s, %s)",
                (nombre, correo, contraseña),
            )
            mysql.connection.commit()
            session["email"] = correo  # crear sesion del email
            return render_template("registro.html", registration_successful=True)
    return render_template("registro.html")


@app.route('/agregar_producto', methods=['POST'])  # insertar datos
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        ganancia = request.form['ganancia']
        existencias = request.form['existencias']
        existencias_deseadas = request.form['existencias_deseadas']
        proveedor = request.form['proveedor']
        categoria = request.form['categoria']

        print(existencias_deseadas)
        if existencias_deseadas == '':
            existencias_deseadas = None

        cur = mysql.connection.cursor()
        # Obtener la fecha y hora actual
        # fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO Producto (Nombre, Precio_Compra, Precio_Venta, Ganancia_Producto, Existencias, Existencias_Deseadas, ID_Provedor, ID_C) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)",
                    (nombre, precio_compra, precio_venta, ganancia, existencias, existencias_deseadas, proveedor, categoria))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('inventario'))


@app.route('/editar_producto/<int:id>', methods=['POST'])
def editar_producto(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        ganancia = request.form['ganancia']
        existencias = request.form['existencias']
        existencias_deseadas = request.form['existencias_deseadas']

        proveedor = request.form['proveedor']
        categoria = request.form['categoria']

        cur.execute("UPDATE producto SET Nombre = %s, Precio_Compra = %s, Precio_Venta = %s, Ganancia_Producto = %s, Existencias = %s, Existencias_Deseadas = %s, ID_Provedor = %s, ID_C= %s  WHERE ID_Producto = %s",
                    (nombre, precio_compra, precio_venta, ganancia, existencias, existencias_deseadas, proveedor, categoria, id))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('inventario'))


@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("DELETE FROM producto WHERE ID_Producto = %s",
                (id,))  # ID_Productos cambia
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario'))


@app.route("/cerrar_sesion")
def cerrar_sesion():
    if "email" in session:
        session.pop("email")
        return render_template("iniciar_sesion.html")
    else:
        return redirect(url_for("iniciar_sesion"))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
