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
from datetime import datetime, timedelta
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


@app.route("/promocional")
def promocional():
    return render_template("inicio/promocional.html")


@app.route("/spinner")
def spinner():
    return render_template("loader.html")


@app.route("/terminosycondiciones")
def terminosycondiciones():
    return render_template("terminosycondiciones.html")


@app.route("/productos")
def productos():
    return render_template("inicio/productos.html")


@app.route("/editar_perfil")
def editar_perfil():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login WHERE Correo = %s", (session["email"],))
    login = cur.fetchone()

    return render_template("editar_perfil.html", login=login)


@app.route('/editar_login', methods=['POST'])
def editar_login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        id = request.form['indice_id']
        user = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Comprobar si el correo ya está registrado
        cur.execute(
            "SELECT * FROM login WHERE Correo = %s AND ID_Login != %s", (correo, id))
        existing_email = cur.fetchone()

        # Comprobar si el usuario ya existe
        cur.execute(
            "SELECT * FROM login WHERE Nombre = %s AND ID_Login != %s", (user, id))
        existing_user = cur.fetchone()

        if existing_email:
            flash("El correo electrónico ya está registrado", "error_email")
            cur.close()
            return redirect(url_for('editar_perfil'))

        elif existing_user:
            flash("El usuario ya existe. Por favor, elija otro", "error_user")
            cur.close()
            return redirect(url_for('editar_perfil'))

        else:
            # Actualizar los datos del usuario
            cur.execute(
                "UPDATE login SET Nombre = %s, Correo = %s, Contraseña = %s WHERE ID_Login = %s",
                (user, correo, contraseña, id)
            )
            mysql.connection.commit()
            cur.close()

            # Actualizar la sesión
            session["email"] = correo

    return redirect(url_for('editar_perfil'))


# Seccion del gestor


@app.route("/tablero")
def tablero():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        query = """
        SELECT
            (SELECT caja.Ingresos_Del_Corte
            FROM caja
            ORDER BY ID_Caja DESC
            LIMIT 1) AS Ingresos_Del_Corte,

            (SELECT caja.Ganancias
            FROM caja
            ORDER BY ID_Caja DESC
            LIMIT 1) AS Ganancias,

            (SELECT caja.Reeinvertir
            FROM caja
            ORDER BY ID_Caja DESC
            LIMIT 1) AS Reeinvertir,

            (SELECT COUNT(*)
            FROM envios
            WHERE envios.ID_StatusE = 3) AS envios,

            (SELECT COUNT(*)
            FROM apartados
            WHERE apartados.ID_Status = 1) AS apartados;
        """
        cur.execute(query)
        data = cur.fetchone()
        # Acceder a los elementos de la tupla correctamente
        if data:
            ingresos_del_corte = data[0]
            ganancias = data[1]
            reeinvertir = data[2]
            envios = data[3]
            apartados = data[4]
        else:
            ingresos_del_corte = None
            ganancias = None
            envios = None
            reeinvertir = None
            apartados = None
        cur.execute("""
        SELECT COUNT(*) AS total_productos
        FROM producto;
        """)
        total_producto = cur.fetchone()
        cur.execute("""
        SELECT COUNT(*) AS total_ventas
            FROM ventas
            JOIN anio_venta ON ventas.ID_AV = anio_venta.ID_AV
            JOIN mes_venta ON ventas.ID_MV  = mes_venta.ID_MV
            JOIN dia_venta ON ventas.ID_DV = dia_venta.ID_DV
            WHERE CURDATE() = STR_TO_DATE(CONCAT(anio_venta.Anio_Venta, '-',
                CASE mes_venta.Mes_Venta
                    WHEN 'Enero' THEN '01'
                    WHEN 'Febrero' THEN '02'
                    WHEN 'Marzo' THEN '03'
                    WHEN 'Abril' THEN '04'
                    WHEN 'Mayo' THEN '05'
                    WHEN 'Junio' THEN '06'
                    WHEN 'Julio' THEN '07'
                    WHEN 'Agosto' THEN '08'
                    WHEN 'Septiembre' THEN '09'
                    WHEN 'Octubre' THEN '10'
                    WHEN 'Noviembre' THEN '11'
                    WHEN 'Diciembre' THEN '12'
                END, '-', dia_venta.Dia_Venta), '%Y-%m-%d');
        """)
        total_ventas = cur.fetchone()
        cur.execute("""
            SELECT COUNT(*) AS total_clientes
            FROM clientes;
        """)
        total_clientes = cur.fetchone()
        cur.execute("""
            SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            apartados.*,
            status_apartados.Status_Apartado,
            producto.ID_Producto,
            producto.Nombre
        FROM
            clientes,
            apartados,
            relacion_c_p_a_e,
            status_apartados,
            producto
        WHERE
            relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            AND relacion_c_p_a_e.ID_Apartado  = apartados.ID_Apartados
            AND relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            AND apartados.ID_Status = status_apartados.ID_Status
            AND status_apartados.ID_Status = 1;
        """)
        deudores = cur.fetchall()
        cur.execute("""
        SELECT
            producto.Nombre,
            producto_venta.ID_Producto,
            COUNT(*) AS cantidad
        FROM
            producto_venta
        JOIN
            producto ON producto_venta.ID_Producto = producto.ID_Producto
        GROUP BY
            producto_venta.ID_Producto, producto.Nombre
        ORDER BY
            cantidad DESC
        LIMIT 5;
        """)
        mas_vendidos = cur.fetchall()
        return render_template("tablero.html", email=session["email"], clientes=clientes, reeinvertir=reeinvertir, ingresos_del_corte=ingresos_del_corte, ganancias=ganancias,
                               envios=envios, mas_vendidos=mas_vendidos, apartados=apartados, deudores=deudores, total_producto=total_producto, total_ventas=total_ventas, total_clientes=total_clientes)
    else:
        return render_template("inicio/iniciar_sesion.html")


# @app.route('/buscar', methods=['POST'])
# def buscar():
#     buscando = request.form.get('buscar')
#     return redirect(url_for('inventario', buscando=buscando))

@app.route("/inventario", methods=['GET'])
def inventario():
    if "email" in session:
        update = request.args.get('update')
        eliminado = request.args.get('eliminado')

        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT
            producto.ID_Producto,
            producto.Nombre,
            producto.Precio_Compra,
            producto.Precio_Venta,
            producto.Ganancia_Producto,
            producto.Existencias,
            producto.Existencias_Deseadas,
            proveedor.ID_Proveedor,
            proveedor.Empresa,
            categorias.ID_C,
            categorias.Categoria
        FROM
            producto
        INNER JOIN
            proveedor ON producto.ID_Provedor = proveedor.ID_Proveedor
        INNER JOIN
            categorias ON producto.ID_C = categorias.ID_C
        ORDER BY
            producto.ID_Producto DESC;
        """)
        Productos = cur.fetchall()
        # Avisos de escasos productos
        cur.execute("""
        SELECT
            producto.Nombre,
            producto.Existencias 
            FROM
            producto
            WHERE producto.Existencias <=5;
        """)
        producto_escaso = cur.fetchall()
        # Actualizar ganancia del producto
        cur.execute("""
        UPDATE 
            producto 
        SET producto.Ganancia_Producto = Precio_Venta - Precio_Compra;
        """)
        mysql.connection.commit()
        # proveedor form
        cur.execute("SELECT ID_Proveedor, Empresa  FROM proveedor")
        Proveedor = cur.fetchall()
        # Categorias form
        cur.execute("SELECT * FROM categorias")
        Categorias = cur.fetchall()
        cur.close()

        return render_template('inventario.html', update=update, eliminado=eliminado, Productos=Productos, Proveedor=Proveedor, Categorias=Categorias, producto_escaso=producto_escaso)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route("/caja", methods=['GET'])
def caja():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT
            caja.*
        FROM
            caja;
        """)
        caja = cur.fetchall()
        cur.close()
        return render_template('caja.html', caja=caja)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/clientes', methods=['GET'])
def clientes():
    if "email" in session:
        cur = mysql.connection.cursor()
        # Ver todos los datos de clientes
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            clientes.Apellido_M,
            clientes.Total_Adeudo,
            clientes.Celular,
            t_apartado.Tiene_Apartados
        FROM
            clientes
        INNER JOIN
            t_apartado ON clientes.ID_TAP = t_apartado.ID_TAP;
        """)
        clientes = cur.fetchall()

        #  Actualizar si tiene o no apartados un cliente segun CPAE
        cur.execute("""
            UPDATE clientes
        SET ID_TAP =
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM relacion_c_p_a_e
                    WHERE relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
                    AND relacion_c_p_a_e.ID_Apartado IS NOT NULL
                ) THEN 1
                ELSE 2
            END;
        """)
        mysql.connection.commit()
        # -- Actualizar el adeudo de un cliente en tabla clientes segun el apartado que tiene
        cur.execute("""
            UPDATE clientes
            SET Total_Adeudo = (
                SELECT apartados.Deuda_Pendiente
                FROM apartados
                JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
                WHERE relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            );
        """)
        mysql.connection.commit()
        cur.execute("SELECT ID_CEL,Celular FROM celulares")
        Telefono = cur.fetchall()
        cur.close()
        return render_template('clientes.html', clientes=clientes, Telefono=Telefono)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/ventas', methods=['GET'])
def ventas():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ventas")
        ventas = cur.fetchall()
        cur.close()
        return render_template('ventas.html', ventas=ventas)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/envios', methods=['GET'])
def envios():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            envios.*,
            destino.Destino,
            producto.ID_Producto,
            producto.Nombre,
            STR_TO_DATE(CONCAT(
                anio_envio.Anio_Envio, '-',
                CASE
                    WHEN mes_envio.Mes_Envio = 'Enero' THEN '01'
                    WHEN mes_envio.Mes_Envio = 'Febrero' THEN '02'
                    WHEN mes_envio.Mes_Envio = 'Marzo' THEN '03'
                    WHEN mes_envio.Mes_Envio = 'Abril' THEN '04'
                    WHEN mes_envio.Mes_Envio = 'Mayo' THEN '05'
                    WHEN mes_envio.Mes_Envio = 'Junio' THEN '06'
                    WHEN mes_envio.Mes_Envio = 'Julio' THEN '07'
                    WHEN mes_envio.Mes_Envio = 'Agosto' THEN '08'
                    WHEN mes_envio.Mes_Envio = 'Septiembre' THEN '09'
                    WHEN mes_envio.Mes_Envio = 'Octubre' THEN '10'
                    WHEN mes_envio.Mes_Envio = 'Noviembre' THEN '11'
                    WHEN mes_envio.Mes_Envio = 'Diciembre' THEN '12'
                END, '-', dia_envio.Dia_Envio), '%Y-%m-%d') AS Fecha_Envio,
            clientes.Apellido_M

        FROM
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN envios ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
            INNER JOIN destino ON envios.ID_Destino = destino.ID_Destino
            INNER JOIN status_envio ON envios.ID_StatusE = status_envio.ID_StatusE
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            INNER JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
            INNER JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
            INNER JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
        WHERE
            envios.ID_StatusE = 3
        ORDER BY
            envios.ID_Envios ASC;
            """)
        envios = cur.fetchall()
        # Obtener clientes para form
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P
        FROM
            clientes;
            """)
        clientes = cur.fetchall()
        # Obtener destino para form
        cur.execute("""
        SELECT
            destino.ID_Destino,
            destino.Destino
        FROM
            destino;
            """)
        destino = cur.fetchall()
        cur.execute("""
        SELECT
            status_envio.ID_StatusE,
            status_envio.Status_Envio
        FROM
            status_envio;
            """)
        status = cur.fetchall()
        cur.execute("""
        SELECT
                colonia.ID_C ,
                colonia.Colonia
            FROM
                colonia;
            """)
        colonia = cur.fetchall()
        cur.execute("""
        SELECT
            producto.ID_Producto,
            producto.Nombre
        FROM
            producto;
            """)
        productos = cur.fetchall()
        # Actualizar dias de envio para los que estan en cpae
        cur.execute("""
        UPDATE envios, dia_envio, mes_envio, anio_envio SET envios.Dias_Para_El_Envio = DATEDIFF(STR_TO_DATE(CONCAT(anio_envio.Anio_Envio, '-',
            CASE mes_envio.Mes_Envio
                WHEN 'Enero' THEN '01'
                WHEN 'Febrero' THEN '02'
                WHEN 'Marzo' THEN '03'
                WHEN 'Abril' THEN '04'
                WHEN 'Mayo' THEN '05'
                WHEN 'Junio' THEN '06'
                WHEN 'Julio' THEN '07'
                WHEN 'Agosto' THEN '08'
                WHEN 'Septiembre' THEN '09'
                WHEN 'Octubre' THEN '10'
                WHEN 'Noviembre' THEN '11'
                WHEN 'Diciembre' THEN '12'
            END, '-', dia_envio.Dia_Envio), '%Y-%m-%D'), CURDATE())
        WHERE
            envios.ID_DE = dia_envio.ID_DE
            AND envios.ID_ME = mes_envio.ID_ME
            AND envios.ID_AE = anio_envio.ID_AE;
        """)
        mysql.connection.commit()
        # Para los clientes marcados en enviar
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            envios.*,
            destino.Destino,
            producto.ID_Producto,
            producto.Nombre,
            STR_TO_DATE(CONCAT(
                anio_envio.Anio_Envio, '-',
                CASE
                    WHEN mes_envio.Mes_Envio = 'Enero' THEN '01'
                    WHEN mes_envio.Mes_Envio = 'Febrero' THEN '02'
                    WHEN mes_envio.Mes_Envio = 'Marzo' THEN '03'
                    WHEN mes_envio.Mes_Envio = 'Abril' THEN '04'
                    WHEN mes_envio.Mes_Envio = 'Mayo' THEN '05'
                    WHEN mes_envio.Mes_Envio = 'Junio' THEN '06'
                    WHEN mes_envio.Mes_Envio = 'Julio' THEN '07'
                    WHEN mes_envio.Mes_Envio = 'Agosto' THEN '08'
                    WHEN mes_envio.Mes_Envio = 'Septiembre' THEN '09'
                    WHEN mes_envio.Mes_Envio = 'Octubre' THEN '10'
                    WHEN mes_envio.Mes_Envio = 'Noviembre' THEN '11'
                    WHEN mes_envio.Mes_Envio = 'Diciembre' THEN '12'
                END, '-', dia_envio.Dia_Envio), '%Y-%m-%d') AS Fecha_Envio,
                clientes.Apellido_M

        FROM
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN envios ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
            INNER JOIN destino ON envios.ID_Destino = destino.ID_Destino
            INNER JOIN status_envio ON envios.ID_StatusE = status_envio.ID_StatusE
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            INNER JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
            INNER JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
            INNER JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
        WHERE
            envios.ID_StatusE = 1
        ORDER BY
            envios.ID_Envios ASC;
        """)
        envios_enviados = cur.fetchall()
        # Para los clientes marcados en cancelar
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            envios.*,
            destino.Destino,
            producto.ID_Producto,
            producto.Nombre,
            STR_TO_DATE(CONCAT(
                anio_envio.Anio_Envio, '-',
                CASE
                    WHEN mes_envio.Mes_Envio = 'Enero' THEN '01'
                    WHEN mes_envio.Mes_Envio = 'Febrero' THEN '02'
                    WHEN mes_envio.Mes_Envio = 'Marzo' THEN '03'
                    WHEN mes_envio.Mes_Envio = 'Abril' THEN '04'
                    WHEN mes_envio.Mes_Envio = 'Mayo' THEN '05'
                    WHEN mes_envio.Mes_Envio = 'Junio' THEN '06'
                    WHEN mes_envio.Mes_Envio = 'Julio' THEN '07'
                    WHEN mes_envio.Mes_Envio = 'Agosto' THEN '08'
                    WHEN mes_envio.Mes_Envio = 'Septiembre' THEN '09'
                    WHEN mes_envio.Mes_Envio = 'Octubre' THEN '10'
                    WHEN mes_envio.Mes_Envio = 'Noviembre' THEN '11'
                    WHEN mes_envio.Mes_Envio = 'Diciembre' THEN '12'
                END, '-', dia_envio.Dia_Envio), '%Y-%m-%d') AS Fecha_Envio,
                clientes.Apellido_M
        FROM
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN envios ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
            INNER JOIN destino ON envios.ID_Destino = destino.ID_Destino
            INNER JOIN status_envio ON envios.ID_StatusE = status_envio.ID_StatusE
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            INNER JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
            INNER JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
            INNER JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
        WHERE
            envios.ID_StatusE = 4
        ORDER BY
            envios.ID_Envios ASC;
        """)
        envios_cancelados = cur.fetchall()
        # Envios entregados
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            envios.*,
            destino.Destino,
            producto.ID_Producto,
            producto.Nombre,
            STR_TO_DATE(CONCAT(
                anio_envio.Anio_Envio, '-',
                CASE
                    WHEN mes_envio.Mes_Envio = 'Enero' THEN '01'
                    WHEN mes_envio.Mes_Envio = 'Febrero' THEN '02'
                    WHEN mes_envio.Mes_Envio = 'Marzo' THEN '03'
                    WHEN mes_envio.Mes_Envio = 'Abril' THEN '04'
                    WHEN mes_envio.Mes_Envio = 'Mayo' THEN '05'
                    WHEN mes_envio.Mes_Envio = 'Junio' THEN '06'
                    WHEN mes_envio.Mes_Envio = 'Julio' THEN '07'
                    WHEN mes_envio.Mes_Envio = 'Agosto' THEN '08'
                    WHEN mes_envio.Mes_Envio = 'Septiembre' THEN '09'
                    WHEN mes_envio.Mes_Envio = 'Octubre' THEN '10'
                    WHEN mes_envio.Mes_Envio = 'Noviembre' THEN '11'
                    WHEN mes_envio.Mes_Envio = 'Diciembre' THEN '12'
                END, '-', dia_envio.Dia_Envio), '%Y-%m-%d') AS Fecha_Envio,
                clientes.Apellido_M
        FROM
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN envios ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
            INNER JOIN destino ON envios.ID_Destino = destino.ID_Destino
            INNER JOIN status_envio ON envios.ID_StatusE = status_envio.ID_StatusE
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            INNER JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
            INNER JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
            INNER JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
        WHERE
            envios.ID_StatusE = 2
        ORDER BY
            envios.ID_Envios ASC;
        """)
        envios_entregados = cur.fetchall()
        # Para los toaster
        cur.execute("""
        SELECT
            envios.Dias_Para_El_Envio
        FROM
            envios
        WHERE
            envios.Dias_Para_El_Envio <=1
            AND  envios.ID_StatusE = 3;

        """)
        pocos_dias = cur.fetchall()
        cur.close()
        return render_template("envios.html", envios_cancelados=envios_cancelados, pocos_dias=pocos_dias, envios=envios, envios_enviados=envios_enviados, envios_entregados=envios_entregados, productos=productos, clientes=clientes, destino=destino, status=status, colonia=colonia)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/apartados', methods=['GET'])
def apartados():
    if "email" in session:
        cur = mysql.connection.cursor()
        # tabla principal
        cur.execute("""
        SELECT 
            clientes.ID_Cliente,
            clientes.Nombres,    
            clientes.Apellido_P,
            clientes.Apellido_M,
            apartados.ID_Apartados,
            apartados.Cantidad_Abonada,
            apartados.Deuda_Pendiente,
            apartados.Dias_Restantes,
            apartados.Fecha_Apartado,
            apartados.Fecha_Limite,
            apartados.Fecha_UltimoPago,    
            apartados.ID_Status,
            status_apartados.Status_Apartado,
            producto.ID_Producto,
            producto.Nombre
        FROM 
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN apartados ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
            INNER JOIN status_apartados ON apartados.ID_Status = status_apartados.ID_Status
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            WHERE 
            status_apartados.ID_Status = 1
        ORDER BY 
            apartados.ID_Apartados ASC;
            """)
        apartados = cur.fetchall()
        cur = mysql.connection.cursor()
        # clientes form
        cur.execute("""
        SELECT 
                clientes.ID_Cliente,
                clientes.Nombres,
                clientes.Apellido_P
            FROM 
                clientes;
            """)
        clientes = cur.fetchall()
        # productos form
        cur.execute("""
        SELECT 
            producto.ID_Producto,
            producto.Nombre  
        FROM 
            producto;
            """)
        productos = cur.fetchall()
        # dias restantes
        cur.execute(
            """
            UPDATE apartados
            SET Dias_Restantes = DATEDIFF(Fecha_Limite, CURDATE());
            """, )
        mysql.connection.commit()
        # deuda pendiente
        cur.execute(
            """
            UPDATE 
                apartados 
            SET 
                apartados.Deuda_Pendiente   = Deuda_Inicial  - Cantidad_Abonada;
            """, )
        mysql.connection.commit()
        cur.close()
        return render_template("apartados.html", productos=productos, clientes=clientes, apartados=apartados)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if "email" in session:
        # verProductos = request.args.get('verProductos')
        idCategoria = request.form.get('idcategoria')
        print("la categora es:", idCategoria)

        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT categorias.ID_C, categorias.Categoria, producto.ID_Producto, producto.Nombre, producto.Existencias
        FROM categorias
        LEFT JOIN producto ON producto.ID_C = categorias.ID_C
        WHERE categorias.ID_C = %s
    """, (idCategoria,))
        verProductos = cur.fetchall()

        cur.execute("""
        SELECT categorias.ID_C , categorias.Categoria , COUNT(producto.ID_Producto) AS total_productos
        FROM categorias
        LEFT JOIN producto ON producto.ID_C = categorias.ID_C
        GROUP BY categorias.ID_C, categorias.Categoria;
        """)
        categorias = cur.fetchall()
        cur.close()
        return render_template('categorias.html', categorias=categorias, verProductos=verProductos)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/proveedor', methods=['GET'])
def proveedor():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Empresa FROM proveedor")
        proveedor = cur.fetchall()
        cur.close()
        return render_template('proveedor.html', proveedor=proveedor)
    else:
        return render_template("inventario.html")


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

        if not existing_email:
            # El correo electrónico no está registrado
            correo_no_encontrado = True
            return render_template("inicio/iniciar_sesion.html", correo_no_encontrado=correo_no_encontrado)
        else:
            # El correo electrónico está registrado
            # En el cuarto campo de la tupla (Contraseña) se compara con la contraseña del Form
            if existing_email[3] == contraseña:
                # Contraseña correcta
                # Crear session email con el email
                session["email"] = correo
                return render_template("inicio/iniciar_sesion.html", user=correo, registration_login=True)
            else:
                # Contraseña incorrecta
                bad_password = True
                return render_template(
                    "inicio/iniciar_sesion.html", bad_password=bad_password, email=correo
                )
    return render_template("inicio/iniciar_sesion.html")


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
                "inicio/registro.html", email_found=email_found, error_message=error_message
            )

        elif existing_user:  # ya exis  te usuario
            user_found = True
            error_message = "El usuario ya existe. Por favor, elija otro"
            return render_template(
                "inicio/registro.html", user_found=user_found, error_message=error_message
            )
        else:
            # registrar en base de datos
            cur.execute(
                "INSERT INTO login (Nombre, Correo, Contraseña, Fecha_Registro) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                (nombre, correo, contraseña)
            )
            mysql.connection.commit()
            session["email"] = correo  # crear sesion del email
            return render_template("inicio/registro.html", registration_successful=True)
    return render_template("inicio/registro.html")


# Agregar productos
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


@app.route('/editar_producto/<int:id>', methods=['POST', 'GET'])
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

        if existencias_deseadas == '':
            existencias_deseadas = None

        # Saber si
        try:
            cur.execute(
                "UPDATE producto SET Nombre = %s, Precio_Compra = %s, Precio_Venta = %s, Ganancia_Producto = %s, Existencias = %s, Existencias_Deseadas = %s, ID_Provedor = %s, ID_C= %s WHERE ID_Producto = %s",
                (nombre, precio_compra, precio_venta, ganancia, existencias,
                 existencias_deseadas, proveedor, categoria, id)
            )
            mysql.connection.commit()
            update = True
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            update = False
        finally:
            cur.close()
        return redirect(url_for('inventario', update=update))


@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("DELETE FROM producto WHERE ID_Producto = %s",
                (id,))  # ID_Productos cambia
    mysql.connection.commit()
    eliminado = True

    cur.close()
    return redirect(url_for('inventario', eliminado=eliminado))


# Agregar Categoria
@app.route('/agregar_categoria', methods=['POST'])  # insertar datos
def agregar_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO categorias (Categoria) VALUES (%s)", (nombre,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('categorias'))


@app.route('/editar_categoria/<int:id>', methods=['POST'])  # Enviar
def editar_categoria(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
    cur.execute(
        "UPDATE categorias SET Categoria = %s WHERE ID_C = %s", (nombre, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('categorias'))


@app.route('/eliminar_categoria', methods=['POST'])
def eliminar_categoria():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("DELETE FROM categorias WHERE ID_C = %s",
                (id,))  # ID_Productos cambia
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('categorias'))

# Agregar Categoria


@app.route('/agregar_cliente', methods=['POST'])  # insertar datos
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_p = request.form['apellido_p']
        apellido_m = request.form['apellido_m']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO clientes (Nombres, Apellido_P, Apellido_M, Celular) VALUES (%s,%s,%s,%s)", (
                nombre, apellido_p, apellido_m, telefono)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes'))


@app.route('/agregar_telefono_cliente', methods=['POST'])  # insertar datos
def agregar_telefono_cliente():
    if request.method == 'POST':
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO celulares (Celular) VALUES (%s)", (telefono,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes'))


@app.route('/editar_cliente/<int:id>', methods=['POST'])  # Enviar
def editar_cliente(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_p = request.form['apellido_p']
        apellido_m = request.form['apellido_m']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE clientes SET Nombres = %s, Apellido_P = %s, Apellido_M = %s, Celular = %s WHERE ID_Cliente = %s", (nombre, apellido_p, apellido_m, telefono, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes'))


@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("DELETE FROM clientes WHERE ID_Cliente = %s",
                (id,))  # ID_Productos cambia
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('clientes'))

# Agregar envio a cleinte


@app.route('/agregar_envio', methods=['POST'])  # insertar datos
def agregar_envio():
    if request.method == 'POST':
        cliente = request.form['cliente']
        producto = request.form['producto']
        # Foraneas para 'relacion_c_p_a_e'
        calle = request.form['calle']
        cruzamiento_1 = request.form['cruzamiento_1']
        cruzamiento_2 = request.form['cruzamiento_2']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        # Obtener el día, mes y año de la fecha
        id_dia = fecha.day
        id_mes = fecha.month
        id_año = fecha.year - 2023
        destino = request.form['destino']
        # status = request.form['status']
        colonia = request.form['colonia']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO envios (Calle, Cruzamiento_1, Cruzamiento_2, ID_DE, ID_ME, ID_AE, ID_Destino, ID_StatusE, ID_C) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (calle, cruzamiento_1, cruzamiento_2, id_dia, id_mes, id_año, destino, 3, colonia))
        mysql.connection.commit()
        # Obtener el último ID insertado en la tabla 'envios'
        cur.execute("SELECT MAX( envios.ID_Envios) FROM envios ;")
        id_envio = cur.fetchone()[0]
        # Insertar en la tabla 'relacion_c_p_a_e'
        cur.execute(
            "INSERT INTO relacion_c_p_a_e (ID_Cliente, ID_Producto, ID_Envio) VALUES (%s, %s, %s)",
            (cliente, producto, id_envio)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('envios'))


@app.route('/agregar_apartado', methods=['POST'])  # insertar datos
def agregar_apartado():
    if request.method == 'POST':
        cliente = request.form['cliente']
        producto = request.form['producto']
        # Foraneas para 'relacion_c_p_a_e'
        # id_editar_apartado = request.form['id_apartado']
        cantidad = request.form['cantidad']
        abonoInicial = request.form['abono']

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Agregar 15 días a la fecha actual
        fecha_limite = fecha_actual + timedelta(days=15)

        # Formatear las fechas a formato 'YYYY-MM-DD'
        fecha_actual = fecha_actual.strftime('%Y-%m-%d')
        fecha_limite = fecha_limite.strftime('%Y-%m-%d')

        cur = mysql.connection.cursor()
        # Obtener la dueda multiplicando producto * cantidad
        cur.execute("""
            SELECT 
                producto.Precio_Venta * %s as Deuda
            FROM 
                producto 
            WHERE 
                producto.ID_Producto = %s;
            """, (cantidad, producto))
        mysql.connection.commit()
        deudaInicial = cur.fetchone()[0]
        # Crear el apartado
        cur.execute(
            "INSERT INTO apartados (Cantidad_Abonada, Deuda_Inicial, ID_Status, Fecha_Apartado,Fecha_Limite ) VALUES (%s, %s, 1, %s,%s)",
            (abonoInicial, deudaInicial, fecha_actual, fecha_limite))
        mysql.connection.commit()
        # Obtener el último ID insertado en la tabla 'apartados'
        cur.execute("SELECT MAX( apartados.ID_Apartados ) FROM apartados;")
        id_apartado = cur.fetchone()[0]
        # Insertar en la tabla 'relacion_c_p_a_e'
        cur.execute(
            "INSERT INTO relacion_c_p_a_e (ID_Cliente, ID_Producto, ID_Apartado) VALUES (%s, %s, %s)",
            (cliente, producto, id_apartado)
        )
        mysql.connection.commit()

        cur.close()
        return redirect(url_for('apartados'))


@app.route('/editar_envio/<int:id>', methods=['POST'])  # Enviar
def editar_envio(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # producto = request.form['producto']
        calle = request.form['calle']
        cruzamiento_1 = request.form['cruzamiento_1']
        cruzamiento_2 = request.form['cruzamiento_2']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        # Obtener el día, mes y año de la fecha
        id_dia = fecha.day
        id_mes = fecha.month
        id_año = fecha.year - 2023
        destino = request.form['destino']
        # como obtener el valor del form si esta deshabiliado
        status = request.form['status']
        colonia = request.form['colonia']
        cur = mysql.connection.cursor()

    cur.execute(
        "UPDATE envios SET Calle = %s,  Cruzamiento_1 = %s,  Cruzamiento_2 = %s, ID_DE = %s, ID_ME = %s,ID_AE = %s ,ID_Destino = %s ,ID_StatusE = %s,ID_C = %s   WHERE ID_Envios = %s",
        (calle, cruzamiento_1, cruzamiento_2, id_dia, id_mes, id_año, destino, status, colonia, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('envios'))


@app.route('/regresar_envio', methods=['POST'])  # Enviar
def regresar_envio():
    if request.method == 'POST':
        id = request.form['indice_id']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE 
            envios 
        SET 
            envios.ID_StatusE = 3
        WHERE 
            envios.ID_Envios = %s;
                    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('envios'))


@app.route('/marcar_enviado', methods=['POST'])
def marcar_enviado():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("""
        UPDATE 
            envios 
        SET 
            envios.ID_StatusE = 1
        WHERE 
            envios.ID_Envios = %s;
    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('envios'))


@app.route('/marcar_entregado', methods=['POST'])
def marcar_entregado():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("""
        UPDATE 
            envios 
        SET 
            envios.ID_StatusE = 2,
            envios.Dias_De_Entregado = CURDATE() 
        WHERE 
            envios.ID_Envios = %s;
    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('envios'))


@app.route('/marcar_cancelado', methods=['POST'])
def marcar_cancelado():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("""
        UPDATE 
            envios 
        SET 
            envios.ID_StatusE = 4
        WHERE 
            envios.ID_Envios = %s;
    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('envios'))


@app.route('/ver_productos_categoria', methods=['POST'])
def ver_productos_categoria():
    cur = mysql.connection.cursor()
    idCategoria = request.form['indice_id']
    # print("El valor de 'id' es:", id)
    cur.execute("""
        SELECT categorias.ID_C, categorias.Categoria, producto.ID_Producto, producto.Nombre, producto.Existencias
        FROM categorias
        LEFT JOIN producto ON producto.ID_C = categorias.ID_C
        WHERE categorias.ID_C = %s
    """, (idCategoria,))
    verProductos = cur.fetchall()
    return redirect(url_for("categorias", verProductos=verProductos))

#  cur.execute("""
#     SELECT
#         Producto.Nombre,
#         categorias.Categoria
#     FROM
#         Producto,
#         categorias
#     WHERE
#         producto.ID_C = categorias.ID_C
#         AND categorias.ID_C  = %s;
# """, (id,))


@app.route("/cerrar_sesion")
def cerrar_sesion():
    if "email" in session:
        session.pop("email")
        return render_template("inicio/iniciar_sesion.html")
    else:
        return redirect(url_for("iniciar_sesion"))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
