from flask import Flask
from flask import render_template
from flask import redirect
from flask.helpers import url_for
from flask_mysqldb import MySQL
from flask import request, session, g
from flask import flash
from controller.mail import enviar_email
from flask_mail import Mail, Message
from flask_login import UserMixin
from controller.config import Config
from models.models import Cliente, Empleado
from datetime import date, datetime

app = Flask(__name__, template_folder= 'templates')
usuEnSesion = None
mail = Mail()

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='libreria_f&f'

mysql = MySQL(app)

class Cliente: 
    def __init__(self, id_cli, usuario_cli, contraseña_cli):
        self.id_cli = id_cli
        self.usuario_cli = usuario_cli
        self.contraseña_cli = contraseña_cli
    def __repr__(self):
        return f'<Cliente: {self.usuario_cli}>'

class Empleado: 
    def __init__(self, id_emp, usuario_emp, contraseña_emp):
        self.id_emp = id_emp
        self.usuario_emp = usuario_emp
        self.contraseña_emp = contraseña_emp
    def _repr_(self):
        return f'<Empleado: {self.usuario_emp}>'


clientes = []
clientes.append(Cliente(id_cli=1, usuario_cli='Franco', contraseña_cli='contraseña'))

empleados = []
empleados.append(Empleado(id_emp=1, usuario_emp='Federico', contraseña_emp='contraseña'))


app.secret_key = 'clavesecreta'


@app.before_request
def before_request():
    if "id_emp" in session:
        Empleado = [x for x in empleados if x.id_emp == session['id_emp']][0]
        g.Empleado = session["id_emp"]
    if "id_cli" in session:
        Cliente = [x for x in clientes if x.id_cli == session['id_cli']][0]
        g.Cliente = session["id_cli"]

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')





@app.route('/login_cliente', methods=['GET', 'POST'])
def ingresoCliente():

    if request.method == 'POST':
        usuario_cli = request.form['usuario_cli']
        contraseña_cli = request.form['contraseña_cli']
        cur = mysql.connection.cursor()
        sQuery = "SELECT usuario_cli, contraseña_cli from cliente where usuario_cli = %s and contraseña_cli = %s"
        cur.execute(sQuery, [usuario_cli, contraseña_cli])
        cliente = cur.fetchone()
        cur.close()
        if cliente != None:
            return redirect(url_for('homeCliente')) 
        else:
            flash('Usuario y/o contraseña incorrectos. Por favor, intente nuevamente')
    return render_template('login_c.html')           
    



@app.route('/login_empleado', methods=['GET','POST'])
def ingresoEmpleado():
    if request.method == 'POST':
        usuario_emp = request.form['usuario_emp']
        contraseña_emp = request.form['contraseña_emp']
        cur = mysql.connection.cursor()
        sQuery = "SELECT usuario_emp, contraseña_emp from empleado where usuario_emp = %s and contraseña_emp = %s"
        cur.execute(sQuery, [usuario_emp, contraseña_emp])
        empleado = cur.fetchone()
        cur.close()
        if empleado != None:
            usuEnSesion = usuario_emp
            return redirect(url_for('homeEmpleado')) 
        else:
            flash('Usuario y/o contraseña incorrectos. Por favor, intente nuevamente')
    return render_template('login_e.html')  



@app.route('/registro_empleado', methods=['GET', 'POST'])
def registroEmpleado():
    if request.method == 'POST': #--> para enviar los datos desde el formulario
        nombre_emp = request.form['nombre_emp']
        apellido_emp = request.form['apellido_emp']
        email_emp = request.form['email_emp']
        usuario_emp = request.form['usuario_emp']
        contraseña_emp = request.form['contraseña_emp']
        fecha_inicio = date.today()

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO empleado (nombre_emp, apellido_emp, email_emp, usuario_emp, contraseña_emp, fecha_inicio) VALUES (%s, %s, %s, %s, %s, %s)',
        (nombre_emp, apellido_emp, email_emp, usuario_emp, contraseña_emp, fecha_inicio))

        mysql.connection.commit()
        return render_template('home_e.html')
    return render_template('registro_e.html')



@app.route('/registro_cliente', methods=['GET', 'POST'])
def registroCliente():
    if request.method == 'POST':
        nombre_cli = request.form['nombre_cli']
        apellido_cli = request.form['apellido_cli']
        email_cli = request.form['email_cli']
        usuario_cli = request.form['usuario_cli']
        contraseña_cli = request.form['contraseña_cli']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cliente (nombre_cli, apellido_cli, email_cli, usuario_cli, contraseña_cli) VALUES (%s, %s, %s, %s, %s)',
        (nombre_cli, apellido_cli, email_cli, usuario_cli, contraseña_cli))

        mysql.connection.commit()

        enviar_email(email_cli, "Bienvenido", "Gracias por registrarte")

        return render_template('home_c.html')#esto no manda a funcion home se queda en registro

    return render_template('registro_c.html')



@app.route('/home_empleado', methods=['GET', 'POST'])
def homeEmpleado():
    return render_template('home_e.html')



@app.route('/home_cliente', methods=['GET', 'POST'])
def homeCliente():
    return render_template('home_c.html')


@app.route('/registro_proveedores', methods=['GET', 'POST'])
def registroProveedores():
    if request.method == 'POST':
        desc_proveedor = request.form['desc_proveedor']
        direccion_proveedor = request.form['direccion_proveedor']
        localidad_proveedor = request.form['localidad_proveedor']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO proveedor (desc_Proveedor, direccion_Proveedor, localidad_Proveedor) VALUES (%s, %s, %s)',
        (desc_proveedor, direccion_proveedor, localidad_proveedor))

        mysql.connection.commit()
        return render_template('home_e.html')
    return render_template('registro_p.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        descripcion_Consulta = request.form['comentarios']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO consulta (usuario_Consulta, descripcion_Consulta, fecha_Consulta) VALUES (fedeBruschi, %s, current_date())',
        (descripcion_Consulta))
        mysql.connection.commit()
        return redirect(url_for('nexoPostconsulta')) 

    return render_template('contacto.html')

@app.route('/muestralibros', methods=['GET', 'POST'])
def mostrarlibros():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_Libro, nombre_Libro, fecha_Publicacion_Libro, concat(nombre_Autor, " ", apellido_Autor), desc_Categoria, desc_Editorial FROM libro JOIN categoria ON libro.categoria_Libro = id_Categoria JOIN editorial ON libro.editorial_Libro = id_Editorial JOIN autor ON libro.autor_Libro = id_Autor')
    libros = cur.fetchall()

    return render_template('muestraLibros.html', libros = libros)

@app.route('/muestraCompras', methods=['GET', 'POST'])
def mostrarCompras():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT fecha_Compra, nombre_Libro, precio_Total_compra FROM compra JOIN libro ON id_Libro_Compra = libro.id_Libro JOIN cliente ON id_Cliente_Compra = cliente.nro_cli WHERE cliente.usuario_cli like fedeBruschi')
    compras = cur.fetchall()

    return render_template('muestraLibros.html', compras = compras)

@app.route('/muestraConsultas', methods=['GET', 'POST'])
def mostrarConsultas():
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT id_Consulta, usuario_Consulta, fecha_Consulta, descripcion_Consulta  FROM consulta')
    consultas = cur.fetchall()

    return render_template('muestraConsultas.html', consultas = consultas)

@app.route('/comprarLibro', methods=['GET', 'POST'])
def comprarLibro():
    cur = mysql.connection.cursor()
    cur.execute('SELECT nombre_Libro, precio_Libro FROM libro WHERE stock_Libro > 0')
    librosCom = cur.fetchall()

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        nombre_lib = request.form['libros_Compra']
        cur.execute('UPDATE libro SET stock_libro = stock_libro - 1 WHERE nombre_Libro like %s', (nombre_lib))
        mysql.connection.commit()
        cur.execute('INSERT INTO compra (fecha_Compra, usuario_Comprador, libro_Comprado) VALUES (current_date(), fedeBruschi, %s) ', (nombre_lib))
        return redirect(url_for('agradecimientoCompra')) 

    return render_template('comprar.html', librosCom = librosCom)

@app.route('/muestralibroscliente', methods=['GET', 'POST'])
def mostrarlibrosCliente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_Libro, nombre_Libro, fecha_Publicacion_Libro, concat(nombre_Autor, " ", apellido_Autor), desc_Categoria, desc_Editorial, ifnull(stock_Libro, 0), precio_Libro FROM libro JOIN categoria ON libro.categoria_Libro = id_Categoria JOIN editorial ON libro.editorial_Libro = id_Editorial JOIN autor ON libro.autor_Libro = id_Autor')
    librosC = cur.fetchall()

    return render_template('muestraLibrosCliente.html', libros = librosC)

@app.route('/registro_libros/', methods=['GET', 'POST'])
def registroLibros():
    if request.method == 'POST':
        nombre_Libro = request.form['nombre_libro']
        fecha_Publicacion_Libro = request.form['fecha_publicacion_libro']
        nombre_autor_Libro = request.form['nombre_autor_libro']
        apellido_autor_Libro = request.form['apellido_autor_Libro']
        categoria_Libro = request.form['categoria_libro']
        editorial_Libro = request.form['editorial_libro']
        stock_Libro = request.form ['stock_libro']

        cur = mysql.connection.cursor()

        id_Autor = cur.execute('SELECT id_Autor FROM autor WHERE nombre_Autor like %s and apellido_Autor like %s', (nombre_autor_Libro, apellido_autor_Libro ))
        id_Categoria = cur.execute("SELECT id_Categoria FROM categoria WHERE nombre_Categoria like %s", (categoria_Libro,))
        id_Editorial = cur.execute("SELECT id_Editorial FROM editorial WHERE desc_Editorial like %s", (editorial_Libro,))

        cur.execute('INSERT INTO libro (nombre_Libro, fecha_Publicacion_Libro, autor_Libro, categoria_Libro, editorial_Libro, stock_Libro) VALUES (%s, %s, %s, %s, %s, %s)',
        (nombre_Libro, fecha_Publicacion_Libro, id_Autor, id_Categoria, id_Editorial, stock_Libro))

        mysql.connection.commit()
    return render_template('registro_l.html')

@app.route('/registro_categorias', methods=['GET', 'POST'])
def registroCategorias():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        desc_categoria = request.form['desc_categoria']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO categoria (nombre_categoria,desc_Categoria) VALUES (%s,%s)', (nombre_categoria, desc_categoria))

        mysql.connection.commit()
    return render_template('registro_ca.html')


@app.route('/registro_autores', methods=['GET', 'POST'])
def registroAutores():
    if request.method == 'POST':
        nombre_autor = request.form['nombre_autor']
        apellido_autor = request.form['apellido_autor']
        fecha_nacimiento_autor = request.form['fecha_nacimiento_autor']
        nacionalidad_autor = request.form['nacionalidad_autor']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO autor (nombre_Autor, apellido_Autor, fecha_Nacimiento_Autor, nacionalidad_Autor) VALUES (%s, %s, %s, %s)',
        (nombre_autor, apellido_autor, fecha_nacimiento_autor, nacionalidad_autor))

        mysql.connection.commit()
    return render_template('registro_a.html')


@app.route('/registro_editoriales', methods=['GET', 'POST'])
def registroEditoriales():
    if request.method == 'POST':
        desc_editorial = request.form['desc_editorial']
        pais_editorial = request.form['pais_editorial']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO editorial (desc_Editorial, pais_Editorial) VALUES (%s, %s)',
        (desc_editorial, pais_editorial))

        mysql.connection.commit()
    return render_template('registro_ed.html')

@app.route('/nexo_postConsulta', methods=['GET', 'POST'])
def nexoPostconsulta():
    return render_template('nexoConsulta.html')

@app.route('/graciasPorComprar', methods=['GET', 'POST'])
def agradecimientoCompra():
    return render_template('agradecimientoCompra.html')


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
