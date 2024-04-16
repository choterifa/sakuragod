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

app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_DB"] = config.MYSQL_DB
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
# Configurar la clave secreta
app.config["SECRET_KEY"] = config.HEX_SEC_KEY
mysql = MySQL(app)


@app.route("/")
def index():
    if "email" in session:
        # si se registro se envia a index
        return render_template("index.html", email=session["email"])
    else:
        return render_template("index.html")


# la ruta igual al action del form
@app.route("/iniciar_sesion", methods=["GET", "POST"])
def sign():
    # if "email" in session:
    #     # si se registro se envia a index
    #     return render_template("index.html", email=session["email"])
    # else:
    if request.method == "POST":  # lo que recibo por post
        email = request.form["email"]  # gaurda el name en variable
        password = request.form["password"]

        cur = mysql.connection.cursor()  # guarda en la variable la conecion
        cur.execute("SELECT * FROM users WHERE email = %s",
                    (email,))  # se pasa la variable email
        existing_email = cur.fetchone()  # si esta guarda la tupla o fila de los datos
        cur.close()
        print(existing_email)

        if not existing_email:
            # El correo electrónico no está registrado
            email_not_found = True
            return render_template("sign.html", email_not_found=email_not_found)
        else:
            # El correo electrónico está registrado
            # en el cuarto campo de contraseña compara la contraseña del form
            if existing_email[3] == password:
                # Contraseña correcta
                # crear session email con el email
                session["email"] = email
                # redireccionar
                return redirect(url_for("successful_login", user=email, registration_login=True))
            else:
                # Contraseña incorrecta
                bad_password = True
                return render_template(
                    "sign.html", bad_password=bad_password, email=email
                )
    return render_template("sign.html")


@app.route("/registro", methods=["GET", "POST"])
def signup():
    # if "email" in session:
    #     return render_template("index.html", email=session["email"])
    # else:
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # comprobar antes si estan en la bd para no registralos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_email = cur.fetchone()

        cur.execute("SELECT * FROM users WHERE name = %s", (name,))
        existing_user = cur.fetchone()

        if existing_email:  # ya existe en bd
            email_found = True
            error_message = "El correo electrónico ya está registrado."
            return render_template(
                "signup.html", email_found=email_found, error_message=error_message
            )

        elif existing_user:  # ya existe usuario
            user_found = True
            error_message = "El usuario ya existe. Por favor, elija otro."
            return render_template(
                "signup.html", user_found=user_found, error_message=error_message
            )
        else:
            # registrar en base de datos
            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password),
            )
            mysql.connection.commit()
            session["email"] = email  # crear sesion del email
            return redirect(
                # mensaje de registro
                url_for("successful_registration",
                        registration_successful=True)
            )
    return render_template("signup.html")


@app.route("/Signout")
def Signout():
    if "email" in session:
        # Obtener el valor de 'email' de la sesión
        email = session.get("email")
        session.pop(
            "email", None
        )  # Eliminar la clave 'email' de la sesión si está presente
        return render_template("sign.html")
    else:
        return redirect(url_for("sign"))


@app.route("/successful_login")
def successful_login():
    registration_login = request.args.get("registration_login")
    if registration_login == "True":
        return render_template("successful_login.html")
    else:
        return index()


@app.route("/successful_registration")
def successful_registration():
    registration_successful = request.args.get("registration_successful")
    if registration_successful == "True":
        return render_template("successful_registration.html")
    else:
        return index()


@app.route("/tasks", methods=['GET'])
def tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('tasks.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO tasks (nombre, descripcion,email,fecha) VALUES (%s, %s, %s, %s)",
                    (nombre, descripcion, session['email'], fecha_actual))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('tasks'))


@app.route('/edit_task/<int:id>', methods=['POST'])
def edit_task(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur.execute("UPDATE tasks SET nombre = %s, descripcion = %s WHERE id = %s",
                    (nombre, descripcion, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('tasks'))


@app.route('/delete_task', methods=['POST'])
def delete_task():
    cur = mysql.connection.cursor()
    id = request.form['task_id']
    print("Valor de id:", id)
    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('tasks'))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
