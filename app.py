from datetime import datetime
import re
from flask import request, redirect, url_for
from flask import (
    Flask,
    get_flashed_messages,
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

        # Validar que el correo electrónico termine en ".com"
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[cC][oO][mM]$", correo):
            flash("El correo electrónico debe terminar en '.com'", "error_email")
            return redirect(url_for('editar_perfil'))

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
            flash("editado", "perfil_editado")
            return redirect(url_for('editar_perfil'))

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

            (SELECT COUNT(*) AS envios
            FROM envios
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
            INNER JOIN clientes ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            WHERE envios.ID_StatusE = 3),

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
        # cur.execute("""
        # SELECT COUNT(*) AS total_ventas
        #     FROM ventas
        #     JOIN anio_venta ON ventas.ID_AV = anio_venta.ID_AV
        #     JOIN mes_venta ON ventas.ID_MV  = mes_venta.ID_MV
        #     JOIN dia_venta ON ventas.ID_DV = dia_venta.ID_DV
        #     WHERE CURDATE() = STR_TO_DATE(CONCAT(anio_venta.Anio_Venta, '-',
        #         CASE mes_venta.Mes_Venta
        #             WHEN 'Enero' THEN '01'
        #             WHEN 'Febrero' THEN '02'
        #             WHEN 'Marzo' THEN '03'
        #             WHEN 'Abril' THEN '04'
        #             WHEN 'Mayo' THEN '05'
        #             WHEN 'Junio' THEN '06'
        #             WHEN 'Julio' THEN '07'
        #             WHEN 'Agosto' THEN '08'
        #             WHEN 'Septiembre' THEN '09'
        #             WHEN 'Octubre' THEN '10'
        #             WHEN 'Noviembre' THEN '11'
        #             WHEN 'Diciembre' THEN '12'
        #         END, '-', dia_venta.Dia_Venta), '%Y-%m-%d');
        # """)
        # total_ventas = cur.fetchone()
        cur.execute("""
            SELECT COUNT(*) AS total_clientes
            FROM clientes;
        """)
        total_clientes = cur.fetchone()
        cur.execute("""
        SELECT
            clientes.Nombres,
            clientes.Apellido_P ,
            clientes.Apellido_M,
            apartados.Deuda_Pendiente
        FROM
            apartados,
            clientes,
            relacion_c_p_a_e
        WHERE
            apartados.ID_Apartados = relacion_c_p_a_e.ID_Apartado
            AND clientes.ID_Cliente = relacion_c_p_a_e.ID_Cliente
        ORDER BY
            Deuda_Pendiente DESC
        LIMIT 6;
        """)
        deudores = cur.fetchall()
        cur.execute("""
        SELECT
            SUM(Deuda_Pendiente) AS Total_Deuda_Pendiente
        FROM
            apartados,
            clientes,
            relacion_c_p_a_e
        WHERE relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
        AND relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente;
        """)
        dineroEnApartados = cur.fetchall()
        cur.execute("""
        SELECT
                producto_venta.ID_Producto,
                producto.Nombre,
                SUM(producto_venta.Cantidad_Vendida) AS cantidad
            FROM
                producto_venta
            JOIN
                producto ON producto_venta.ID_Producto = producto.ID_Producto
            GROUP BY
                producto_venta.ID_Producto, producto.Nombre
            ORDER BY
                cantidad DESC
            LIMIT 6;
        """)
        mas_vendidos = cur.fetchall()
        # Cantidad de ventas del dia
        cur.execute("""
        SELECT
            COUNT(*) as 'Ventas del dia'
        FROM
            ventas
        WHERE
            Fecha_Venta = CURDATE()
            AND ID_Devuelto = 2;
        """)
        ventas_dia = cur.fetchone()[0]
        cur.execute("""
        SELECT SUM(ventas.Ingresos_Total) as totalvendido
        FROM ventas
        WHERE CURDATE() = Fecha_Venta ;
        """)
        ventas_dia_cantidad = cur.fetchone()[0]
        cur.execute("""
        SELECT SUM(ventas.Ganancia_Total ) as Ganancia_Total
        FROM ventas
        WHERE CURDATE() = Fecha_Venta ;
        """)
        Ganancia_Total = cur.fetchone()[0]
        # Objetivo del dai
        cur.execute(
            "SELECT COALESCE(Objetivo, 0) FROM objetivo_ventas WHERE Fecha = CURDATE()"
        )
        objetivo_hoy = cur.fetchone()[0]

        # Calcular el porcentaje
        if objetivo_hoy > 0:
            porcentaje = (ventas_dia / objetivo_hoy) * 100
            # Redondear al número entero más próximo
            porcentaje = round(porcentaje)
            restante = 100 - porcentaje
            if restante < 0:
                restante = 0  # Que no sea negativo
        else:
            porcentaje = 0
            restante = 100  # Si el objetivo es cero, el porcentaje restante es 100%
        print(porcentaje, restante)

        cur.close()
        return render_template("tablero.html", Ganancia_Total=Ganancia_Total, ventas_dia_cantidad=ventas_dia_cantidad, restante=restante, porcentaje=porcentaje, email=session["email"], ventas_dia=ventas_dia, dineroEnApartados=dineroEnApartados, clientes=clientes, reeinvertir=reeinvertir, ingresos_del_corte=ingresos_del_corte, ganancias=ganancias,
                               envios=envios, mas_vendidos=mas_vendidos, apartados=apartados, deudores=deudores, total_producto=total_producto, total_clientes=total_clientes)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/establecer_objetivo', methods=['POST'])
def establecer_objetivo():
    if request.method == 'POST':
        objetivo = request.form['objetivo']
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        cur = mysql.connection.cursor()

        # Comprobar si ya existe un objetivo para la fecha actual
        cur.execute(
            "SELECT ID_Objetivo FROM objetivo_ventas WHERE Fecha = %s", [fecha_actual])
        resultado = cur.fetchone()

        if resultado:
            # Actualizar el objetivo existente
            cur.execute(
                "UPDATE objetivo_ventas SET Objetivo = %s WHERE ID_Objetivo = %s",
                (objetivo, resultado[0])
            )
        else:
            # Insertar un nuevo objetivo
            cur.execute(
                "INSERT INTO objetivo_ventas (Fecha, Objetivo) VALUES (%s, %s)",
                (fecha_actual, objetivo)
            )

        mysql.connection.commit()
        cur.close()

        # Redirigir a la página principal o donde desees
        return redirect(url_for('tablero'))


# @app.route('/buscar', methods=['POST'])
# def buscar():
#     buscando = request.form.get('buscar')
#     return redirect(url_for('inventario', buscando=buscando))

@app.route("/inventario", methods=['GET'])
def inventario():
    if "email" in session:
        # eliminado = request.args.get('eliminado')

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
        cur.execute("""
        SELECT
            producto.ID_Producto,
            producto.Nombre,
            producto.Existencias_Deseadas - producto.Existencias AS 'productos faltantes'
        FROM producto;
        """)
        rellenar_a_deseado = cur.fetchall()
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

        return render_template('inventario.html', rellenar_a_deseado=rellenar_a_deseado, Productos=Productos, Proveedor=Proveedor, Categorias=Categorias, producto_escaso=producto_escaso)
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
            t_apartado ON clientes.ID_TAP = t_apartado.ID_TAP
        ORDER BY
            clientes.ID_Cliente DESC;
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
                SELECT SUM(apartados.Deuda_Pendiente)
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
        cur.execute("""
        SELECT
            ventas.ID_Venta,
            producto_venta.ID_Producto,
            producto.Nombre,
            producto_venta.Cantidad_Vendida,
            ventas.Hora,
            ventas.Fecha_Venta,
            ventas.Ingresos_Total,
            ventas.Ganancia_Total,
            ventas.Reinversion_Total,
            ventas.ID_FP,
            forma_pago.Forma_De_Pago,
            ventas.ID_FVenta,
            forma_de_venta.Status_Venta,
            ventas.ID_Devuelto,
            devuelto.Devolucion
        FROM
            ventas
            INNER JOIN producto_venta ON producto_venta.ID_Venta = ventas.ID_Venta
            INNER JOIN producto ON producto_venta.ID_Producto = producto.ID_Producto
            INNER JOIN forma_de_venta ON ventas.ID_FVenta = forma_de_venta.ID_StatusV
            INNER JOIN forma_pago ON ventas.ID_FP = forma_pago.ID_FP
            INNER JOIN devuelto ON ventas.ID_Devuelto = devuelto.ID_Devolucion
	        WHERE producto_venta.ID_Devuelto  = 2
            ORDER BY ventas.ID_Venta DESC ;
        """)
        ventas = cur.fetchall()
        print(ventas)
        # Ventas devueltas
        cur.execute("""
        SELECT
            ventas.ID_Venta,
            producto_venta.ID_Producto,
            producto.Nombre,
            producto_venta.Cantidad_Vendida,
            ventas.Hora,
            ventas.Fecha_Venta,
            ventas.Ingresos_Total,
            ventas.Ganancia_Total,
            ventas.Reinversion_Total,
            ventas.ID_FP,
            forma_pago.Forma_De_Pago,
            ventas.ID_FVenta,
            forma_de_venta.Status_Venta,
            ventas.ID_Devuelto,
            devuelto.Devolucion,
            producto_venta.Cantidad_Regresada,
	        producto_venta.Monto_Regresado
        FROM
            ventas
            INNER JOIN producto_venta ON producto_venta.ID_Venta = ventas.ID_Venta
            INNER JOIN producto ON producto_venta.ID_Producto = producto.ID_Producto
            INNER JOIN forma_de_venta ON ventas.ID_FVenta = forma_de_venta.ID_StatusV
            INNER JOIN forma_pago ON ventas.ID_FP = forma_pago.ID_FP
            INNER JOIN devuelto ON ventas.ID_Devuelto = devuelto.ID_Devolucion
            WHERE producto_venta.ID_Devuelto  = 1
            ORDER BY ventas.ID_Venta DESC ;
        """)
        ventasDevueltas = cur.fetchall()

        cur.execute("""
        SELECT
            producto.ID_Producto,
            producto.Nombre
        FROM
            producto;
            """)
        productos = cur.fetchall()
        cur.execute("""
            SELECT *
            FROM forma_pago;
            """)
        forma_pago = cur.fetchall()
        cur.execute("""
        SELECT CURDATE();
            """)
        fecha_actual = cur.fetchone()[0]

        devuelto = get_flashed_messages(category_filter=['devuelto'])
        cantidad_posible_dev = request.args.get('proveedorCorte')

        cur.close()
        return render_template('ventas.html', cantidad_posible_dev=cantidad_posible_dev, fecha_actual=fecha_actual, ventasDevueltas=ventasDevueltas, devuelto=devuelto, forma_pago=forma_pago, productos=productos, ventas=ventas)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/agregar_venta', methods=['POST'])
def agregar_venta():
    if request.method == 'POST':

        forma_pago = request.form['forma_pago']
        id_producto = request.form['producto']
        cantidad = request.form['cantidad']

        # Obtener la hora y la fecha actuales
        ahora = datetime.now()
        hora = ahora.strftime("%H:%M:%S")
        fecha_venta = ahora.strftime("%Y-%m-%d")

        cur = mysql.connection.cursor()

        # Generar una venta vacia con fecha
        cur.execute("INSERT INTO ventas (Hora, Fecha_Venta, ID_FP, ID_FVenta, ID_Devuelto) VALUES (%s, %s, %s, %s, %s)",
                    (hora, fecha_venta, forma_pago, 1, 2))
        mysql.connection.commit()

        # Obtener id ultimo
        id_venta = cur.lastrowid
        print("id_venta", id_venta)

        # Insertar datos en producto_venta
        cur.execute("INSERT INTO producto_venta (ID_Producto, ID_Venta, Cantidad_Vendida, ID_Devuelto) VALUES (%s, %s, %s,%s)",
                    (id_producto, id_venta, cantidad, 2))
        mysql.connection.commit()
        # Rellenar datos pv
        cur.execute("""
        UPDATE producto_venta
        JOIN (
            SELECT MAX(ID_PV) AS Ultimo_ID_PV
            FROM producto_venta
            WHERE ID_Producto = %s
        ) AS ultima_fila ON producto_venta.ID_PV = ultima_fila.Ultimo_ID_PV
        JOIN producto ON producto_venta.ID_Producto = producto.ID_Producto
        SET producto_venta.Subtotal_Vendido = producto.Precio_Venta * producto_venta.Cantidad_Vendida,
            producto_venta.Subtotal_Reinversión = producto.Precio_Compra * \
                producto_venta.Cantidad_Vendida,
            producto_venta.Subtotal_Ganancia = producto.Ganancia_Producto * \
                producto_venta.Cantidad_Vendida
        WHERE producto.ID_Producto = %s;
        """, (id_producto, id_producto))
        mysql.connection.commit()

        # Update ventas con suma de todos los porudcot en esa venta
        cur.execute("""
        UPDATE ventas
            JOIN (
                SELECT
                    ID_Venta,
                    SUM(Subtotal_Vendido) AS Ingresos_Total,
                    SUM(Subtotal_Ganancia) AS Ganancia_Total,
                    SUM(Subtotal_Reinversión) AS Reinversion_Total,
                    SUM(Cantidad_Vendida) AS Cantidad_Piezas_Vendidas
                FROM producto_venta
                GROUP BY ID_Venta
            ) AS totales ON ventas.ID_Venta = totales.ID_Venta
            SET ventas.Ingresos_Total = totales.Ingresos_Total,
                ventas.Ganancia_Total = totales.Ganancia_Total,
                ventas.Reinversion_Total = totales.Reinversion_Total,
                ventas.Cantidad_Piezas_Vendidas = totales.Cantidad_Piezas_Vendidas
            WHERE ventas.ID_Venta = %s;
        """, (id_venta,))
        mysql.connection.commit()

        # Actualizar inventario
        cur.execute("""
        UPDATE producto
        JOIN (
            SELECT ID_Producto, MAX(ID_PV) AS Ultimo_ID_PV
            FROM producto_venta
            WHERE ID_Producto = %s
            GROUP BY ID_Producto
        ) AS ultima_venta ON producto.ID_Producto = ultima_venta.ID_Producto
        JOIN producto_venta ON producto_venta.ID_PV = ultima_venta.Ultimo_ID_PV
        SET producto.Existencias = producto.Existencias - producto_venta.Cantidad_Vendida
        WHERE producto.ID_Producto = %s;
        """, (id_producto, id_producto))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('ventas'))
    else:
        return redirect(url_for('ventas'))


@app.route('/editar_venta', methods=['POST'])
def editar_venta():
    if request.method == 'POST':

        id_venta = request.form['id_venta']
        id_producto = request.form['producto']
        cantidad = request.form['cantidad']

        cur = mysql.connection.cursor()

        # Insertar datos en producto_venta
        cur.execute("INSERT INTO producto_venta (ID_Producto, ID_Venta, Cantidad_Vendida, ID_Devuelto) VALUES (%s, %s, %s,%s)",
                    (id_producto, id_venta, cantidad, 2))
        mysql.connection.commit()

        # Rellenar datos pv
        cur.execute("""
        UPDATE producto_venta
        JOIN (
            SELECT MAX(ID_PV) AS Ultimo_ID_PV
            FROM producto_venta
            WHERE ID_Producto = %s
        ) AS ultima_fila ON producto_venta.ID_PV = ultima_fila.Ultimo_ID_PV
        JOIN producto ON producto_venta.ID_Producto = producto.ID_Producto
        SET producto_venta.Subtotal_Vendido = producto.Precio_Venta * producto_venta.Cantidad_Vendida,
            producto_venta.Subtotal_Reinversión = producto.Precio_Compra * \
                producto_venta.Cantidad_Vendida,
            producto_venta.Subtotal_Ganancia = producto.Ganancia_Producto * \
                producto_venta.Cantidad_Vendida
        WHERE producto.ID_Producto = %s;
        """, (id_producto, id_producto))
        mysql.connection.commit()

        # Update ventas con suma de todos los porudcot en esa venta
        cur.execute("""
        UPDATE ventas
            JOIN (
                SELECT
                    ID_Venta,
                    SUM(Subtotal_Vendido) AS Ingresos_Total,
                    SUM(Subtotal_Ganancia) AS Ganancia_Total,
                    SUM(Subtotal_Reinversión) AS Reinversion_Total,
                    SUM(Cantidad_Vendida) AS Cantidad_Piezas_Vendidas
                FROM producto_venta
                GROUP BY ID_Venta
            ) AS totales ON ventas.ID_Venta = totales.ID_Venta
            SET ventas.Ingresos_Total = totales.Ingresos_Total,
                ventas.Ganancia_Total = totales.Ganancia_Total,
                ventas.Reinversion_Total = totales.Reinversion_Total,
                ventas.Cantidad_Piezas_Vendidas = totales.Cantidad_Piezas_Vendidas
            WHERE ventas.ID_Venta = %s;
        """, (id_venta,))
        mysql.connection.commit()
        # Actualizar inventario
        cur.execute("""
        UPDATE producto
        JOIN (
            SELECT ID_Producto, MAX(ID_PV) AS Ultimo_ID_PV
            FROM producto_venta
            WHERE ID_Producto = %s
            GROUP BY ID_Producto
        ) AS ultima_venta ON producto.ID_Producto = ultima_venta.ID_Producto
        JOIN producto_venta ON producto_venta.ID_PV = ultima_venta.Ultimo_ID_PV
        SET producto.Existencias = producto.Existencias - producto_venta.Cantidad_Vendida
        WHERE producto.ID_Producto = %s;
        """, (id_producto, id_producto))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('ventas'))
    else:
        return redirect(url_for('ventas'))


@app.route('/envios', methods=['GET'])
def envios():
    if "email" in session:

        cur = mysql.connection.cursor()
        # Tabla general
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
            INNER JOIN apartados ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
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
        cur.execute("""
        SELECT
                clientes.ID_Cliente,
                clientes.Nombres,
                clientes.Apellido_P,
                envios.Dias_Para_El_Envio,
                destino.Destino,
                producto.Nombre,
                envios.ID_Envios
                FROM
                clientes
                INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
                INNER JOIN envios ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
                INNER JOIN destino ON envios.ID_Destino = destino.ID_Destino
                INNER JOIN status_envio ON envios.ID_StatusE = status_envio.ID_StatusE
                INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
                INNER JOIN apartados ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
                INNER JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
                INNER JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
                INNER JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
            WHERE
                envios.ID_StatusE = 03
            ORDER BY
                envios.ID_Envios
                LIMIT 4;
            """)
        proximosEnvios = cur.fetchall()
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
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN envios ON relacion_c_p_a_e.ID_Envio = envios.ID_Envios
            INNER JOIN destino ON envios.ID_Destino = destino.ID_Destino
            INNER JOIN status_envio ON envios.ID_StatusE = status_envio.ID_StatusE
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            INNER JOIN apartados ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
            INNER JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
            INNER JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
            INNER JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
        WHERE
            envios.Dias_Para_El_Envio <=1
            AND  envios.ID_StatusE = 3;
        """)
        pocos_dias = cur.fetchall()
        cur.close()

        return render_template("envios.html", proximosEnvios=proximosEnvios, envios_cancelados=envios_cancelados, pocos_dias=pocos_dias, envios=envios, envios_enviados=envios_enviados, envios_entregados=envios_entregados, productos=productos, clientes=clientes, destino=destino, status=status, colonia=colonia)
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
            producto.Nombre,
            apartados.Cantidad_Comprada
        FROM
            clientes
            INNER JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            INNER JOIN apartados ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
            INNER JOIN status_apartados ON apartados.ID_Status = status_apartados.ID_Status
            INNER JOIN producto ON relacion_c_p_a_e.ID_Producto = producto.ID_Producto
            WHERE
            status_apartados.ID_Status = 1
        ORDER BY
            apartados.ID_Apartados DESC;
            """)
        apartados = cur.fetchall()
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            clientes.Apellido_M,
            apartados.ID_Apartados,
            apartados.Cantidad_Abonada,
            apartados.Deuda_Inicial,
            # apartados.Dias_Restantes,
            apartados.Fecha_Apartado,
            apartados.Fecha_Limite,
            apartados.Fecha_UltimoPago,
            apartados.Fecha_Pagada,
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
            status_apartados.ID_Status = 2
        ORDER BY
            apartados.ID_Apartados ASC;
            """)
        apartadosPagados = cur.fetchall()
        cur.execute("""
        SELECT
            clientes.ID_Cliente,
            clientes.Nombres,
            clientes.Apellido_P,
            clientes.Apellido_M,
            apartados.ID_Apartados,
            apartados.Fecha_Cancelada,
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
            status_apartados.ID_Status = 3
        ORDER BY
            apartados.ID_Apartados ASC;
            """)
        apartadosCancelados = cur.fetchall()
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
        cur.execute("""
        SELECT
            clientes.Nombres,
            clientes.Apellido_P,
            apartados.Dias_Restantes
        FROM
            clientes,
            apartados,
            relacion_c_p_a_e
        WHERE
            clientes.ID_Cliente = relacion_c_p_a_e.ID_Cliente
            AND apartados.ID_Apartados = relacion_c_p_a_e.ID_Apartado
            AND apartados.Dias_Restantes <=2;
            """)
        pocosDiasApartado = cur.fetchall()
        # dias restantes actualizar
        cur.execute(
            """
            UPDATE apartados
            SET Dias_Restantes = DATEDIFF(Fecha_Limite, CURDATE());
            """, )
        mysql.connection.commit()
        # deuda pendiente actualizar
        cur.execute(
            """
            UPDATE
                apartados
            SET
                apartados.Deuda_Pendiente  = Deuda_Inicial  - Cantidad_Abonada;
            """, )
        mysql.connection.commit()
        cur.close()

        return render_template("apartados.html", apartadosCancelados=apartadosCancelados, apartadosPagados=apartadosPagados, pocosDiasApartado=pocosDiasApartado, productos=productos, clientes=clientes, apartados=apartados)
    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/ver_abonos', methods=['POST'])
def ver_abonos():
    cur = mysql.connection.cursor()
    id_apartado = request.form['id_apartado']
    cur.execute("""
        SELECT abonos.ID_Abono,abonos.Fecha, abonos.Cantidad_Abonada
        FROM abonos
        WHERE abonos.ID_Apartado = %s
        ORDER BY abonos.ID_Abono DESC;
    """, (id_apartado,))
    abonos = cur.fetchall()

    if abonos:
        # Formatear la fecha en Python antes de pasarla a la plantilla
        abonos_formateados = [{'fecha': abono[1].strftime(
            "%d/%m/%Y"), 'cantidad': abono[2]} for abono in abonos]

        # Guardar cada abono formateado en un mensaje flash con una categoría 'abono'
        for abono in abonos_formateados:
            flash(abono, 'abono')
        cur.close()
    else:
        flash('No hay abonos para este apartado.', 'abono')

    return redirect(url_for('apartados'))


@app.route('/abonar_apartado', methods=['POST'])
def abonar_apartado():
    if "email" in session:
        id_apartado = request.form['indice_id']
        cantidad_abono = float(
            request.form['cantidad_abono'])  # Convertir a float

        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT
            apartados.Deuda_Pendiente
        FROM apartados
        WHERE ID_Apartados  = %s;
        """, (id_apartado,))
        limiteAbono = cur.fetchone(
        )[0]  # Extraer el primer elemento de la tupla

        if cantidad_abono <= limiteAbono:
            # Actualizar abono
            cur.execute("""
            UPDATE apartados
            SET Cantidad_Abonada = COALESCE(Cantidad_Abonada, 0) + %s,
            Deuda_Pendiente = Deuda_Pendiente - %s
            WHERE ID_Apartados = %s;
            """, (cantidad_abono, cantidad_abono, id_apartado))
            mysql.connection.commit()

            # Generar abono en tabla abonos para poder vizualizarlos luego
            cur.execute("""
            INSERT INTO abonos (ID_Apartado, Fecha, Cantidad_Abonada)
            VALUES (%s, CURDATE(), %s);
            """, (id_apartado, cantidad_abono))
            mysql.connection.commit()

            # Marcar como completado si el adeudo llega a 0
            cur.execute("""
            UPDATE apartados
            SET ID_Status = 2, Fecha_Pagada = CURDATE()
            WHERE Deuda_Pendiente = 0 AND ID_Apartados = %s;
            """, (id_apartado,))
            mysql.connection.commit()
            flash('Abono realizado con éxito.', 'abono_exitoso')
        else:
            flash('La cantidad de abono no puede exceder el límite.', 'abono_fallido')

        cur.close()

    return redirect(url_for('apartados'))


@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if "email" in session:
        # verProductos = request.args.get('verProductos')
        idCategoria = request.form.get('idcategoria')
        # print("la categora es:", idCategoria)

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
        # Mensajes flash
        agregar_categoria = get_flashed_messages(
            category_filter=['agregar_categoria'])
        categoria_editada = get_flashed_messages(
            category_filter=['categoria_editada'])
        categoria_eliminada = get_flashed_messages(
            category_filter=['categoria_eliminada'])
        return render_template('categorias.html', categoria_eliminada=categoria_eliminada, categoria_editada=categoria_editada, categorias=categorias, verProductos=verProductos, agregar_categoria=agregar_categoria)

    else:
        return render_template("inicio/iniciar_sesion.html")


@app.route('/proveedor', methods=['GET'])
def proveedor():
    if "email" in session:
        cur = mysql.connection.cursor()
        # Tabla general
        cur.execute("""
        SELECT
            proveedor.ID_Proveedor,
            proveedor.Empresa,
            proveedor.Monto_Comprado,
            proveedor.Cantidad_Comprada,
            proveedor.ID_RE1 as reparto1,
            reparto1.Dia_Reparto as Dia_Reparto1,
            proveedor.ID_RE2 as reparto2,
            reparto2.Dia_Reparto as Dia_Reparto2
        FROM
            proveedor
        LEFT JOIN
            reparto AS reparto1 ON proveedor.ID_RE1 = reparto1.ID_REP
        LEFT JOIN
            reparto AS reparto2 ON proveedor.ID_RE2 = reparto2.ID_REP;
        """)
        proveedor = cur.fetchall()
        # Dia reparto form
        cur.execute("""
        SELECT * FROM  reparto ;
        """)
        reparto = cur.fetchall()
        cur.close()
        reset = get_flashed_messages(category_filter=['success'])

        # Obtiene el valor de la variable proveedor de la URL

        return render_template("proveedor.html", reparto=reparto, proveedor=proveedor, reset=reset)
    else:
        return render_template("proveedor.html")


@app.route('/reset_proveedor', methods=['POST'])
def reset_proveedor():
    if "email" in session:
        cur = mysql.connection.cursor()
        # Tabla general
        # cur.execute("""
        # SELECT
        #     proveedor.Empresa,
        #     SUM(proveedor.Cantidad_Comprada) AS Cantidad_Total_Comprada,
        #     SUM(proveedor.Monto_Comprado) AS Monto_Total_Comprado
        # FROM
        #     proveedor
        # GROUP BY
        #     proveedor.Empresa;
        # """)
        # proveedorCorte = cur.fetchall()
        # Reset
        cur.execute("""
        UPDATE proveedor
        SET proveedor.Cantidad_Comprada = 0, proveedor.Monto_Comprado = 0;
        """)
        mysql.connection.commit()
        cur.close()
        flash('Proveedor restablecido con éxito', 'success')
        return redirect(url_for('proveedor'))

    else:
        return render_template("proveedor.html")


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
# @app.route('/agregar_producto', methods=['POST'])  # insertar datos
# def agregar_producto():
#     if request.method == 'POST':
#         nombre = request.form['nombre'].strip()
#         precio_compra = request.form['precio_compra'].strip()
#         precio_venta = request.form['precio_venta'].strip()
#         # ganancia = request.form['ganancia']
#         existencias = request.form['existencias'].strip()
#         existencias_deseadas = request.form['existencias_deseadas'].strip()
#         proveedor = request.form['proveedor']
#         categoria = request.form['categoria']

#         if existencias_deseadas == '':
#             existencias_deseadas = None

#         cur = mysql.connection.cursor()
#         # Obtener la fecha y hora actual
#         # fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         cur.execute("INSERT INTO Producto (Nombre, Precio_Compra, Precio_Venta,  Existencias, Existencias_Deseadas, ID_Provedor, ID_C) VALUES (%s, %s, %s,%s,%s,%s,%s)",
#                     (nombre, precio_compra, precio_venta, existencias, existencias_deseadas, proveedor, categoria))
#         mysql.connection.commit()
#         cur.close()
#         return redirect(url_for('inventario'))

# Agregar productos 2


@app.route('/agregar_producto', methods=['POST'])  # insertar datos
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio_compra = request.form['precio_compra'].strip()
        precio_venta = request.form['precio_venta'].strip()
        existencias = request.form['existencias'].strip()
        existencias_deseadas = request.form['existencias_deseadas'].strip()
        proveedor = request.form['proveedor']
        categoria = request.form['categoria']

        if existencias_deseadas == '':
            existencias_deseadas = None

        cur = mysql.connection.cursor()

        try:
            # Verificar si ya existe un producto con el mismo nombre
            cur.execute("SELECT * FROM Producto WHERE Nombre = %s", (nombre,))
            existing_producto = cur.fetchone()

            if existing_producto:
                flash("El producto ya existe", "existing_producto")
            else:
                # Verificar si el producto antes fue eliminado
                cur.execute("""
                    SELECT Nombre
                    FROM productos_eliminados
                    WHERE Nombre LIKE %s;
                """, (nombre,))
                existente_producto_eliminado = cur.fetchone()

                # Si existe, restaurarlo
                if existente_producto_eliminado:
                    cur.execute("""
                        INSERT INTO Producto (Nombre, Precio_Compra, Precio_Venta, Existencias, Existencias_Deseadas, ID_Provedor, ID_C)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (nombre, precio_compra, precio_venta, existencias, existencias_deseadas, proveedor, categoria))
                    mysql.connection.commit()

                    # Eliminar de la tabla de productos eliminados
                    cur.execute("""
                        DELETE FROM productos_eliminados WHERE Nombre = %s;
                    """, (nombre,))
                    mysql.connection.commit()
                else:
                    # Si no está en productos_eliminados, agregar directamente
                    cur.execute("""
                        INSERT INTO Producto (Nombre, Precio_Compra, Precio_Venta, Existencias, Existencias_Deseadas, ID_Provedor, ID_C)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (nombre, precio_compra, precio_venta, existencias, existencias_deseadas, proveedor, categoria))
                    mysql.connection.commit()
                    flash("El producto se agrego", "producto_agregado")

        except Exception as e:
            flash("Error al agregar el producto: " + str(e), "error")
        finally:
            cur.close()
        return redirect(url_for('inventario'))


@app.route('/editar_producto/<int:id>', methods=['POST', 'GET'])
def editar_producto(id):
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        existencias = request.form['existencias']
        existencias_deseadas = request.form['existencias_deseadas']
        proveedor = request.form['proveedor']
        categoria = request.form['categoria']

        if existencias_deseadas == '':
            existencias_deseadas = None

        cur = mysql.connection.cursor()
        try:
            # Verificar si el nuevo nombre del producto ya existe, excluyendo el producto que se está editando
            cur.execute(
                """
                SELECT * FROM producto
                WHERE Nombre = %s AND ID_Producto != %s
                """,
                (nombre, id)
            )
            existing_producto = cur.fetchone()

            if existing_producto:
                flash("Ya existe un producto con el mismo nombre.",
                      "existing_producto")
            else:
                # Realizar la actualización del producto
                cur.execute(
                    """
                    UPDATE producto
                    SET Nombre = %s, Precio_Compra = %s, Precio_Venta = %s, Existencias = %s,
                        Existencias_Deseadas = %s, ID_Provedor = %s, ID_C = %s
                    WHERE ID_Producto = %s
                    """,
                    (nombre, precio_compra, precio_venta, existencias,
                     existencias_deseadas, proveedor, categoria, id)
                )
                mysql.connection.commit()
                flash("El producto fue editado con éxito.", "producto_editado")
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
        finally:
            cur.close()
        return redirect(url_for('inventario'))

    return redirect(url_for('inventario'))


# @app.route('/reabastecer/<int:id>', methods=['POST'])
# def reabastecer(id):
#     cur = mysql.connection.cursor()
#     if request.method == 'POST':
#         resurtirCantidad = request.form['resurtirCantidad']
#         cur.execute(
#             "UPDATE producto SET  Existencias = %s WHERE ID_Producto = %s",
#             (resurtirCantidad, id)
#         )
#         mysql.connection.commit()
#         cur.close()
#     return redirect(url_for('inventario'))


@app.route('/reabastecer', methods=['POST'])
def reabastecer():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        product_ids = request.form.getlist('product_id')
        resurtirCantidades = request.form.getlist('resurtirCantidad')

        for product_id, resurtirCantidad in zip(product_ids, resurtirCantidades):
            # Convertir resurtirCantidad a entero
            resurtirCantidad = int(resurtirCantidad)

            # Obtener las existencias actuales del producto
            cur.execute(
                "SELECT Existencias, ID_Provedor, Precio_Compra FROM producto WHERE ID_Producto = %s",
                (product_id,)
            )
            producto = cur.fetchone()
            existencias_actuales = producto[0]
            id_proveedor = producto[1]
            precio_compra = producto[2]

            # Calcular la cantidad reabastecida
            cantidad_reabastecida = resurtirCantidad - existencias_actuales

            # Asegurarse de que la cantidad reabastecida sea positiva
            if cantidad_reabastecida > 0:
                # Calcular el monto comprado
                monto_comprado = precio_compra * cantidad_reabastecida

                # Actualizar las existencias del producto
                cur.execute(
                    "UPDATE producto SET Existencias = %s WHERE ID_Producto = %s",
                    (resurtirCantidad, product_id)
                )

                # Actualizar el proveedor con la cantidad comprada y el monto comprado
                cur.execute(
                    "UPDATE proveedor SET Cantidad_Comprada = Cantidad_Comprada + %s, Monto_Comprado = Monto_Comprado + %s WHERE ID_Proveedor = %s",
                    (cantidad_reabastecida, monto_comprado, id_proveedor)
                )

        mysql.connection.commit()
        cur.close()
    return redirect(url_for('inventario'))


@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    cur = mysql.connection.cursor()
    id_producto = request.form['indice_id']

    # Obtener el nombre del producto antes de eliminarlo
    cur.execute(
        "SELECT Nombre FROM producto WHERE ID_Producto = %s", (id_producto,))
    nombre_producto = cur.fetchone()[0]

    # Verificar si el producto está siendo utilizado en la tabla relacion_c_p_a_e
    cur.execute("""
        SELECT COUNT(*) FROM relacion_c_p_a_e WHERE ID_Producto = %s
    """, (id_producto,))
    num_usos = cur.fetchone()[0]

    if num_usos > 0:
        flash("No se puede eliminar el producto porque está siendo utilizado en la tabla de relaciones.", "producto_en_uso")
    else:
        # Si el producto no está siendo utilizado, proceder con la eliminación
        cur.execute("DELETE FROM producto WHERE ID_Producto = %s",
                    (id_producto,))
        mysql.connection.commit()

        # Insertar el nombre del producto en la tabla de productos eliminados
        cur.execute(
            "INSERT INTO productos_eliminados (Nombre) VALUES (%s)", (nombre_producto,))
        mysql.connection.commit()

        flash("El producto fue eliminado exitosamente.", "producto_eliminado")

    cur.close()
    return redirect(url_for('inventario'))


# @app.route('/eliminar_producto', methods=['POST'])
# def eliminar_producto():
#     cur = mysql.connection.cursor()

#     try:
#         id_producto = request.form['id_producto']

#         # Verificar si el producto está siendo utilizado en la tabla relacion_c_p_a_e
#         cur.execute("""
#             SELECT COUNT(*) FROM relacion_c_p_a_e WHERE ID_Producto = %s
#         """, (id_producto,))
#         num_usos = cur.fetchone()[0]
#         print(num_usos)

#         if num_usos > 0:
#             flash("No se puede eliminar el producto porque está siendo utilizado en la tabla de relaciones.", "producto_en_uso")
#         else:
#             # Tomar el nombre del producto
#             cur.execute("""
#                 SELECT Nombre FROM producto WHERE ID_Producto = %s
#             """, (id_producto,))
#             producto_eliminado = cur.fetchone()

#             if producto_eliminado:
#                 # Mandar a tabla de productos eliminados
#                 cur.execute("""
#                     INSERT INTO productos_eliminados ( Nombre) VALUES ( %s)
#                 """, (producto_eliminado[0]))
#                 mysql.connection.commit()

#                 # Marcar el producto como eliminado lógicamente
#                 cur.execute("DELETE FROM producto WHERE ID_Producto = %s", (id_producto,))
#                 mysql.connection.commit()

#                 flash("El producto fue eliminado exitosamente.",
#                     "producto_eliminado")
#             else:
#                 flash("No se encontró el producto.", "error")
#     except Exception as e:
#         flash("Error al eliminar el producto: " + str(e), "error")
#     finally:
#         cur.close()

#     return redirect(url_for('inventario'))


# Agregar Categoria


@app.route('/agregar_categoria', methods=['POST'])  # insertar datos
def agregar_categoria():
    if request.method == 'POST':
        # Eliminar espacios en blanco al principio y al final
        nombre = request.form['nombre'].strip()

        cur = mysql.connection.cursor()
        # Validar si ya existe (datos duplicados)
        cur.execute("SELECT * FROM categorias WHERE Categoria = %s", (nombre,))
        existing_categoria = cur.fetchone()

        if existing_categoria:  # Redireccionar
            flash("Nombre registrado", "existing_categoria")
            return redirect(url_for('categorias'))
        else:
            # Obtener si la categoria antes fue eliminada
            cur.execute("""
                SELECT Nombre 
                FROM categorias_eliminadas 
                WHERE Nombre LIKE %s;            
            """, (nombre,))
            existente_categoria_eliminada = cur.fetchone()

            # Si existe, la intercambia de tabla
            if existente_categoria_eliminada:
                cur.execute("""
                    INSERT INTO categorias (Categoria) VALUES (%s);
                """, (nombre,))
                mysql.connection.commit()

                # Eliminar de la tabla
                cur.execute("""
                    DELETE FROM categorias_eliminadas WHERE Nombre = %s;
                """, (nombre,))
                mysql.connection.commit()

            else:
                # Si no está en categorias_eliminadas, agregar directamente
                cur.execute("""
                    INSERT INTO categorias (Categoria) VALUES (%s);
                """, (nombre,))
                mysql.connection.commit()

            flash("La categoria se agrego", "agregar_categoria")
        cur.close()
        return redirect(url_for('categorias'))


# @app.route('/agregar_proveedor', methods=['POST'])  # insertar datos
# def agregar_proveedor():
#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         reparto1 = request.form['reparto1']
#         reparto2 = request.form['reparto2']

#         if reparto2 == '':
#             reparto2 = None

#         cur = mysql.connection.cursor()
#         cur.execute(
#             "INSERT INTO proveedor (Empresa,ID_RE1, ID_RE2) VALUES (%s,%s,%s)", (nombre, reparto1, reparto2))
#         mysql.connection.commit()
#         flash("Agregado", "proveedor_agregado")
#         cur.close()
#         return redirect(url_for('proveedor'))

@app.route('/agregar_proveedor', methods=['POST'])  # insertar datos
def agregar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        reparto1 = request.form['reparto1']

        # Verificar si reparto2 está presente en el formulario
        reparto2 = request.form.get('reparto2', None)

        cur = mysql.connection.cursor()

        try:
            # Verificar si el proveedor ya existe
            cur.execute(
                "SELECT * FROM proveedor WHERE Empresa = %s", (nombre,))
            existing_proveedor = cur.fetchone()

            if existing_proveedor:
                flash("El proveedor ya existe, no es posible agregarlo",
                      "existing_proveedor")
            else:
                # Verificar si el proveedor antes fue eliminado
                cur.execute(
                    "SELECT Empresa FROM proveedor_eliminado WHERE Empresa LIKE %s", (nombre,))
                existente_proveedor_eliminado = cur.fetchone()

                # Si existe, lo restaura y no lo agrega como nuevo proveedor
                if existente_proveedor_eliminado:
                    cur.execute(
                        "INSERT INTO proveedor (Empresa, ID_RE1, ID_RE2) VALUES (%s, %s, %s)", (nombre, reparto1, reparto2))
                    mysql.connection.commit()

                    # Eliminar de la tabla de proveedores eliminados
                    cur.execute(
                        "DELETE FROM proveedor_eliminado WHERE Empresa = %s", (nombre,))
                    mysql.connection.commit()
                    flash("Proveedor agregado exitosamente.",
                          "proveedor_restaurado")
                else:
                    # Insertar en la tabla de proveedores directo sino existe
                    cur.execute(
                        "INSERT INTO proveedor (Empresa, ID_RE1, ID_RE2) VALUES (%s, %s, %s)", (nombre, reparto1, reparto2))
                    mysql.connection.commit()

                    flash("Proveedor agregado exitosamente.",
                          "proveedor_agregado")
        except Exception as e:
            flash("Error al agregar proveedor: " + str(e), "error")
        finally:
            cur.close()

        return redirect(url_for('proveedor'))


# Editar Categoria


@app.route('/editar_categoria/<int:id>', methods=['POST'])  # Enviar
def editar_categoria(id):
    if request.method == 'POST':
        # Eliminar espacios en blanco al principio y al final
        nombre = request.form['nombre'].strip()

        cur = mysql.connection.cursor()

        try:
            # Verificar si la nueva categoría ya existe
            cur.execute("""
                SELECT * FROM categorias 
                WHERE Categoria = %s AND ID_C != %s
            """, (nombre, id))
            existing_categoria = cur.fetchone()

            if existing_categoria:
                flash("Ya existe una categoría con el mismo nombre.",
                      "existing_categoria")
            else:
                # Realizar la actualización de la categoría
                cur.execute(
                    "UPDATE categorias SET Categoria = %s WHERE ID_C = %s", (nombre, id))
                mysql.connection.commit()
                flash("La categoría fue editada con éxito :)",
                      "categoria_editada")
        except Exception as e:
            flash("Error al editar la categoría: " + str(e), "error")
        finally:
            cur.close()

        return redirect(url_for('categorias'))


# @app.route('/editar_proveedor/<int:id>', methods=['POST'])  # Enviar
# def editar_proveedor(id):
#     cur = mysql.connection.cursor()
#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         reparto1 = request.form['reparto1']
#         reparto2 = request.form['reparto2']
#         cur.execute(
#             "UPDATE proveedor SET Empresa = %s, ID_RE1 = %s, ID_RE2 = %s WHERE ID_Proveedor = %s", (nombre, reparto1, reparto2, id))
#         mysql.connection.commit()
#         flash("Editado", "proveedor_editada")
#         cur.close()
#     return redirect(url_for('proveedor'))


@app.route('/editar_proveedor/<int:id>', methods=['POST'])  # Enviar
def editar_proveedor(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        reparto1 = request.form['reparto1']
        # reparto2 = request.form['reparto2']

        # Verificar si reparto2 está presente en el formulario
        reparto2 = request.form.get('reparto2', None)

        try:
            # Verificar si el proveedor editado ya existe
            cur.execute("""
                SELECT * FROM proveedor 
                WHERE Empresa = %s AND ID_Proveedor != %s
            """, (nombre, id))
            existing_proveedor = cur.fetchone()

            if existing_proveedor:
                flash("Ya existe un proveedor con el mismo nombre.",
                      "existing_proveedor")
            else:
                # Realizar la actualización del proveedor
                cur.execute("""
                    UPDATE proveedor 
                    SET Empresa = %s, ID_RE1 = %s, ID_RE2 = %s 
                    WHERE ID_Proveedor = %s
                """, (nombre, reparto1, reparto2, id))
                mysql.connection.commit()
                flash("El proveedor fue editado con éxito.", "proveedor_editado")
        except Exception as e:
            flash("Error al editar el proveedor: " + str(e), "error")
        finally:
            cur.close()

    return redirect(url_for('proveedor'))


@app.route('/eliminar_categoria', methods=['POST'])
def eliminar_categoria():
    cur = mysql.connection.cursor()

    try:
        id = request.form['indice_id']

        # Verificar si hay productos que utilizan esta categoría
        cur.execute("""
            SELECT COUNT(*) FROM producto WHERE ID_C = %s
        """, (id,))
        num_productos = cur.fetchone()[0]

        if num_productos > 0:
            flash(
                "No se puede eliminar la categoría porque hay productos que la utilizan.", "tiene_productos")
        else:
            # Tomar el nombre de la categoría
            cur.execute("""
                SELECT Categoria FROM categorias WHERE ID_C = %s
            """, (id,))
            categoria_eliminada = cur.fetchone()

            if categoria_eliminada:
                # Mandar a tabla eliminada
                cur.execute("""
                    INSERT INTO categorias_eliminadas (Nombre) VALUE (%s)
                """, (categoria_eliminada,))
                mysql.connection.commit()

                # Borrar de verdad
                cur.execute("DELETE FROM categorias WHERE ID_C = %s", (id,))
                mysql.connection.commit()

                flash("La categoría fue eliminada exitosamente.",
                      "categoria_eliminada")
            else:
                flash("No se encontró la categoría.", "error")
    except Exception as e:
        flash("Error al eliminar la categoría: " + str(e), "error")
    finally:
        cur.close()

    return redirect(url_for('categorias'))


@app.route('/eliminar_proveedor', methods=['POST'])
def eliminar_proveedor():
    cur = mysql.connection.cursor()

    try:
        id = request.form['indice_id']

        # Verificar si hay productos que utilizan este proveedor
        cur.execute("""
            SELECT COUNT(*) FROM producto WHERE ID_Provedor = %s
        """, (id,))
        num_productos = cur.fetchone()[0]

        if num_productos > 0:
            flash(
                "No se puede eliminar el proveedor porque hay productos que lo utilizan.", "tiene_productos")
        else:
            # Tomar el nombre del proveedor
            cur.execute("""
                SELECT Empresa FROM proveedor WHERE ID_Proveedor = %s
            """, (id,))
            proveedor_eliminado = cur.fetchone()

            if proveedor_eliminado:
                # Mandar a tabla eliminada
                cur.execute("""
                    INSERT INTO proveedor_eliminado (Empresa) VALUE (%s)
                """, (proveedor_eliminado,))
                mysql.connection.commit()

                # Borrar de verdad
                cur.execute(
                    "DELETE FROM proveedor WHERE ID_Proveedor = %s", (id,))
                mysql.connection.commit()

                flash("El proveedor fue eliminado exitosamente.",
                      "proveedor_eliminado")
            else:
                flash("No se encontró el proveedor.", "error")
    except Exception as e:
        flash("Error al eliminar el proveedor: " + str(e), "error")
    finally:
        cur.close()

    return redirect(url_for('proveedor'))


# Agregar Categoria


@app.route('/agregar_cliente', methods=['POST'])  # insertar datos
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido_p = request.form['apellido_p'].strip()
        apellido_m = request.form['apellido_m'].strip()
        telefono = request.form['telefono'].strip()
        cur = mysql.connection.cursor()

        # Validar si ya existe (datos duplicados)
        cur.execute("""
            SELECT * FROM clientes 
            WHERE Nombres = %s AND Apellido_P = %s AND Apellido_M = %s
        """, (nombre, apellido_p, apellido_m))
        existing_cliente = cur.fetchone()

        if existing_cliente:  # Redireccionar
            flash("El cliente ya está registrado", "existing_cliente")
            return redirect(url_for('clientes'))
        else:
            # Obtener si el cliente antes fue eliminado
            cur.execute("""
                SELECT * FROM clientes_eliminados 
                WHERE Nombres = %s AND ApellidoP = %s AND ApellidoM = %s;            
            """, (nombre, apellido_p, apellido_m))
            existente_cliente_eliminado = cur.fetchone()

            # Si existe, la intercambia de tabla
            if existente_cliente_eliminado:
                cur.execute("""
                    INSERT INTO clientes (Nombres, Apellido_P, Apellido_M, Celular) 
                    VALUES (%s, %s, %s, %s);
                """, (nombre, apellido_p, apellido_m, telefono))
                mysql.connection.commit()

                # Eliminar de la tabla clientes_eliminados
                cur.execute("""
                    DELETE FROM clientes_eliminados 
                    WHERE ID_ClienteEliminado = %s;
                """, (existente_cliente_eliminado[0],))
                mysql.connection.commit()
            else:
                # Si no está en clientes_eliminados, agregar directamente
                cur.execute("""
                    INSERT INTO clientes (Nombres, Apellido_P, Apellido_M, Celular) 
                    VALUES (%s, %s, %s, %s);
                """, (nombre, apellido_p, apellido_m, telefono))
                mysql.connection.commit()

        flash("El cliente se agregó con éxito", "agregar_cliente")

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
        # clientes = cur.fetchall()

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
                SELECT SUM(apartados.Deuda_Pendiente)
                FROM apartados
                JOIN relacion_c_p_a_e ON relacion_c_p_a_e.ID_Apartado = apartados.ID_Apartados
                WHERE relacion_c_p_a_e.ID_Cliente = clientes.ID_Cliente
            );
        """)
        mysql.connection.commit()
        flash("editado", "cliente_agregado")
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
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido_p = request.form['apellido_p'].strip()
        apellido_m = request.form['apellido_m'].strip()
        telefono = request.form['telefono'].strip()

        cur = mysql.connection.cursor()

        try:
            # Verificar si el cliente editado ya existe (solo verificar nombres y apellidos)
            cur.execute("""
                SELECT * FROM clientes 
                WHERE Nombres = %s AND Apellido_P = %s AND Apellido_M = %s AND ID_Cliente != %s
            """, (nombre, apellido_p, apellido_m, id))
            existing_cliente = cur.fetchone()

            if existing_cliente:
                flash(
                    "Ya existe un cliente con los mismos nombres y apellidos.", "existing_cliente")
            else:
                # Realizar la actualización del cliente
                cur.execute("""
                    UPDATE clientes 
                    SET Nombres = %s, Apellido_P = %s, Apellido_M = %s, Celular = %s 
                    WHERE ID_Cliente = %s
                """, (nombre, apellido_p, apellido_m, telefono, id))
                mysql.connection.commit()
                flash("El cliente fue editado con éxito.", "cliente_editado")
        except Exception as e:
            flash("Error al editar el cliente: " + str(e), "error")
        finally:
            cur.close()

        return redirect(url_for('clientes'))


@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']

    # Tomar los datos del cliente
    cur.execute("""
        SELECT Nombres, Apellido_P, Apellido_M 
        FROM clientes  
        WHERE ID_Cliente = %s;
    """, (id,))
    cliente_eliminado = cur.fetchone()
    print(cliente_eliminado)

    # Mandar a la tabla clientes_eliminados
    cur.execute("""
        INSERT INTO clientes_eliminados (Nombres, ApellidoP, ApellidoM) 
        VALUES (%s, %s, %s);
    """, (cliente_eliminado[0], cliente_eliminado[1], cliente_eliminado[2]))
    mysql.connection.commit()

    # Borrar de la tabla clientes
    cur.execute("DELETE FROM clientes WHERE ID_Cliente = %s", (id,))
    mysql.connection.commit()

    flash("El cliente fue eliminado :(", "cliente_eliminado")

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
        # Saber si tiene o no apartado
        cur.execute("""
            SELECT 
                CASE 
                    WHEN ID_Apartado IS NOT NULL THEN 'Tiene apartado'
                    ELSE 'No tiene apartado'
                END AS Estado_Apartado,
                ID_Apartado
            FROM 
                relacion_c_p_a_e
            WHERE 
                ID_Cliente = %s
                AND ID_Producto = %s
            ORDER BY
                ID_Apartado DESC 
            LIMIT 1;
        """, (cliente, producto))
        resultado = cur.fetchone()

        if resultado and resultado[0] == 'Tiene apartado':
            id_apartado = resultado[1]
            print("El cliente tiene un apartado.")
            cur.execute(
                "INSERT INTO envios (Calle, Cruzamiento_1, Cruzamiento_2, ID_DE, ID_ME, ID_AE, ID_Destino, ID_StatusE, ID_C) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (calle, cruzamiento_1, cruzamiento_2, id_dia, id_mes, id_año, destino, 3, colonia))
            mysql.connection.commit()
            # Obtener el último ID insertado en la tabla 'envios'
            cur.execute("SELECT MAX(ID_Envios) FROM envios;")
            id_envio = cur.fetchone()[0]
            # Insertar en la tabla 'relacion_c_p_a_e'
            cur.execute(
                """
                UPDATE 
                    relacion_c_p_a_e
                SET 
                    ID_Envio = %s 
                WHERE 
                    ID_Cliente = %s AND ID_Apartado = %s AND ID_Producto = %s;
                """, (id_envio, cliente, id_apartado, producto))
            mysql.connection.commit()
            # Actualizar días de envío para los que están en cpae
            cur.execute("""
            UPDATE envios
            JOIN dia_envio ON envios.ID_DE = dia_envio.ID_DE
            JOIN mes_envio ON envios.ID_ME = mes_envio.ID_ME
            JOIN anio_envio ON envios.ID_AE = anio_envio.ID_AE
            SET envios.Dias_Para_El_Envio = DATEDIFF(
                STR_TO_DATE(CONCAT(anio_envio.Anio_Envio, '-',
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
                    END, '-', dia_envio.Dia_Envio), '%Y-%m-%d'), CURDATE())
            """)
            mysql.connection.commit()
            flash("editado.","envio_creado")
            
        else:
            flash("El cliente no tiene un apartado, créalo antes.",
                  "no_tiene_apartado")
            cur.close()

    return redirect(url_for('envios'))



@app.route('/agregar_apartado', methods=['POST'])  # insertar datos
def agregar_apartado():
    if request.method == 'POST':
        cliente = request.form['cliente']
        producto = request.form['producto']
        cantidad = request.form['cantidad'].strip()
        abonoInicial = request.form['abono'].strip()

        # Convertir abonoInicial a float
        try:
            abonoInicial = float(abonoInicial)
        except ValueError:
            flash("El abono inicial debe ser un número válido.", "abono_invalido")
            return redirect(url_for('apartados'))

        # Obtener la fecha actual
        fecha_actual = datetime.now()
        # Agregar 15 días a la fecha actual
        fecha_limite = fecha_actual + timedelta(days=15)
        # Formatear las fechas a formato 'YYYY-MM-DD'
        fecha_actual = fecha_actual.strftime('%Y-%m-%d')
        fecha_limite = fecha_limite.strftime('%Y-%m-%d')

        cur = mysql.connection.cursor()
        # Obtener la dueda = multiplicando producto * cantidad
        cur.execute("""
            SELECT 
                producto.Precio_Venta * %s as Deuda
            FROM 
                producto 
            WHERE 
                producto.ID_Producto = %s;
            """, (cantidad, producto))
        deudaInicial = cur.fetchone()[0]

        if abonoInicial >= deudaInicial:
            flash("No es necesario", "abono_excedido")
            return redirect(url_for('apartados'))
        else:
            # Crear el apartado
            cur.execute(
                "INSERT INTO apartados (Cantidad_Abonada, Deuda_Inicial, ID_Status, Fecha_Apartado,Fecha_Limite, Cantidad_Comprada ) VALUES (%s, %s, 1, %s,%s, %s)",
                (abonoInicial, deudaInicial, fecha_actual, fecha_limite, cantidad))
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
            # dias restantes actualizar
            cur.execute(
                """
                UPDATE apartados
                SET Dias_Restantes = DATEDIFF(Fecha_Limite, CURDATE());
                """, )
            mysql.connection.commit()
            # deuda pendiente actualizar
            cur.execute(
                """
                UPDATE
                    apartados
                SET
                    apartados.Deuda_Pendiente  = Deuda_Inicial  - Cantidad_Abonada;
                """, )
            mysql.connection.commit()
            flash("exito", "apartado_creado")

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
        # status = request.form['status']
        colonia = request.form['colonia']
        cur = mysql.connection.cursor()

    cur.execute(
        "UPDATE envios SET Calle = %s,  Cruzamiento_1 = %s,  Cruzamiento_2 = %s, ID_DE = %s, ID_ME = %s,ID_AE = %s ,ID_Destino = %s,ID_C = %s   WHERE ID_Envios = %s",
        (calle, cruzamiento_1, cruzamiento_2, id_dia, id_mes, id_año, destino, colonia, id))
    mysql.connection.commit()

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
    flash("Editado", "envio_editado")
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
    flash("cancelado","envio_cancelado")
    cur.close()
    return redirect(url_for('envios'))


@app.route('/marcar_devuelto', methods=['POST'])
def marcar_devuelto():
    cur = mysql.connection.cursor()
    id_venta = request.form['id_venta2']
    id_producto = request.form['id_producto']
    cantidad_vendida = request.form['cantidadMax']

    cur = mysql.connection.cursor()

    # Obtener cantidad posible a devolver
    # cur.execute("""
    # SELECT Cantidad_Vendida FROM producto_venta WHERE ID_Producto = %s AND ID_Venta = %s;
    # """, (id_producto, id_venta))
    # cantidad_posible_dev = cur.fetchone()

    # Devolver la cantidad de cada producto al inventario
    cur.execute("""
        UPDATE producto 
        SET Existencias = Existencias + %s 
        WHERE ID_Producto = %s;
    """, (cantidad_vendida, id_producto))
    mysql.connection.commit()

    # Update cantidad en pv
    cur.execute("""
    UPDATE producto_venta SET Cantidad_Vendida = Cantidad_Vendida - %s, Cantidad_Regresada = %s,
    Monto_Regresado = Subtotal_Vendido 
    WHERE ID_Venta = %s AND ID_Producto = %s;    
    """, (cantidad_vendida, cantidad_vendida, id_venta, id_producto))
    mysql.connection.commit()

    # Update hora de devuelto y fecha
    cur.execute("""
    UPDATE ventas 
    SET Fecha_Devuelto = CURDATE(), Hora_Devuelto  = NOW()
    WHERE ID_Venta = %s;
    """, (id_venta,))
    mysql.connection.commit()

    # Restar en pv la cantidad restada

    # Obtener el producto y cantidade vendidos de la venta
    # cur.execute("""
    #     SELECT Cantidad_Vendida
    #     FROM producto_venta
    #     WHERE ID_Venta = %s AND ID_Producto = %s ;
    # """, (id_venta, id_producto))
    # productos_vendidos = cur.fetchall()
    # cantidad_vendida = cur.fetchone()

    # for producto in productos_vendidos:
    #     id_producto = producto[0]
    #     cantidad_vendida = producto[1]

    # Obtener la cantidad si solo se regresa alguno de los items pero no todos
    cur.execute("""
    SELECT Cantidad_Vendida FROM producto_venta WHERE ID_Producto = %s AND ID_Venta = %s; 
    """, (id_producto, id_venta))
    cantidad_vendida_restante = cur.fetchone()[0]
    print("cantidad_vendida_restante", cantidad_vendida_restante)

    # Si se regreso todo si se marca como devuelto sino solo actualiza
    if cantidad_vendida_restante == 0:
        # Marcar la venta como devuelta
        cur.execute("""
        UPDATE producto_venta  
        SET ID_Devuelto  = 1, Subtotal_Vendido = 0, Subtotal_Reinversión=0, Subtotal_Ganancia=0
        WHERE ID_Venta = %s AND ID_Producto = %s;
        """, (id_venta, id_producto))
        mysql.connection.commit()

        cur.execute("""
        UPDATE producto_venta 
        SET Hora_Devuelto = NOW(), Fecha_Devuelto = CURDATE()
        WHERE ID_Venta = %s AND ID_Producto = %s;
        """, (id_venta, id_producto))
        mysql.connection.commit()

        # Update ventas con suma de todos los porudcot en esa venta
        cur.execute("""
        UPDATE ventas
            JOIN (
                SELECT 
                    ID_Venta,
                    SUM(Subtotal_Vendido) AS Ingresos_Total,
                    SUM(Subtotal_Ganancia) AS Ganancia_Total,
                    SUM(Subtotal_Reinversión) AS Reinversion_Total,
                    SUM(Cantidad_Vendida) AS Cantidad_Piezas_Vendidas
                FROM producto_venta
                GROUP BY ID_Venta
            ) AS totales ON ventas.ID_Venta = totales.ID_Venta
            SET ventas.Ingresos_Total = totales.Ingresos_Total,
                ventas.Ganancia_Total = totales.Ganancia_Total,
                ventas.Reinversion_Total = totales.Reinversion_Total,
                ventas.Cantidad_Piezas_Vendidas = totales.Cantidad_Piezas_Vendidas
            WHERE ventas.ID_Venta = %s; 
        """, (id_venta,))
        mysql.connection.commit()
    else:
        # Update pv
        cur.execute("""
        UPDATE producto_venta
        JOIN (
            SELECT MAX(ID_PV) AS Ultimo_ID_PV
            FROM producto_venta
            WHERE ID_Producto = %s
        ) AS ultima_fila ON producto_venta.ID_PV = ultima_fila.Ultimo_ID_PV
        JOIN producto ON producto_venta.ID_Producto = producto.ID_Producto
        SET producto_venta.Subtotal_Vendido = producto.Precio_Venta * producto_venta.Cantidad_Vendida,
            producto_venta.Subtotal_Reinversión = producto.Precio_Compra * producto_venta.Cantidad_Vendida,
            producto_venta.Subtotal_Ganancia = producto.Ganancia_Producto * producto_venta.Cantidad_Vendida
        WHERE producto.ID_Producto = %s;
        """, (id_producto, id_producto))
        mysql.connection.commit()

        # Update ventas con suma de todos los porudcot en esa venta
        cur.execute("""
        UPDATE ventas
            JOIN (
                SELECT 
                    ID_Venta,
                    SUM(Subtotal_Vendido) AS Ingresos_Total,
                    SUM(Subtotal_Ganancia) AS Ganancia_Total,
                    SUM(Subtotal_Reinversión) AS Reinversion_Total,
                    SUM(Cantidad_Vendida) AS Cantidad_Piezas_Vendidas
                FROM producto_venta
                GROUP BY ID_Venta
            ) AS totales ON ventas.ID_Venta = totales.ID_Venta
            SET ventas.Ingresos_Total = totales.Ingresos_Total,
                ventas.Ganancia_Total = totales.Ganancia_Total,
                ventas.Reinversion_Total = totales.Reinversion_Total,
                ventas.Cantidad_Piezas_Vendidas = totales.Cantidad_Piezas_Vendidas
            WHERE ventas.ID_Venta = %s; 
        """, (id_venta,))
        mysql.connection.commit()
    flash('La venta se marcó como devolución', 'devuelto')
    cur.close()
    return redirect(url_for('ventas'))


@app.route('/cancelar_apartado', methods=['POST'])
def cancelar_apartado():
    cur = mysql.connection.cursor()
    id = request.form['indice_id']
    cur.execute("""
        UPDATE 
            apartados 
        set 
            apartados.ID_Status = 3
        WHERE 
            apartados.ID_Apartados =%s;
    """, (id,))
    mysql.connection.commit()
    cur.execute("""
        UPDATE 
            apartados 
        set 
            apartados.Fecha_Cancelada  = CURDATE()
        WHERE 
            apartados.ID_Apartados =%s;
    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('apartados'))


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
